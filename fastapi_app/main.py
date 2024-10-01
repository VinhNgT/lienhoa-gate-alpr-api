from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, File, UploadFile
from fastapi.responses import JSONResponse, PlainTextResponse
from openalpr import Alpr
import imghdr
import json
from fastapi_app.models import RequestResponse
import requests
from io import BytesIO
from fake_useragent import UserAgent

alpr = Alpr("vn", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
alpr.set_top_n(5)

ua = UserAgent()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if alpr.is_loaded():
        alpr.unload()


app = FastAPI(
    title="LienHoa auto parking gate ALPR API",
    version="1.0.0",
    summary="API xử lý nhận diện biển số xe.",
    contact={
        "name": "Nguyễn Thế Vinh",
        "url": "https://github.com/VinhNgT",
        "email": "victorpublic0000@gmail.com",
    },
    lifespan=lifespan,
)


@app.post(
    "/process_file",
    summary="Nhận diện biển số xe từ ảnh",
    response_model=RequestResponse,
)
def process_file(file: UploadFile):
    image_type = imghdr.what(file.file)
    if image_type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not a valid image.",
        )

    # Process the image with ALPR
    file.file.seek(0)
    result = alpr.recognize_array(file.file.read())

    return RequestResponse(**result)


@app.get(
    "/process_link/",
    summary="Nhận diện biển số xe từ link ảnh",
    response_model=RequestResponse,
)
def process_link(link: str):
    response = requests.get(link, headers={"User-Agent": ua.chrome})
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to download image from the provided link. Reason: {response.reason}",
        )

    image_data = BytesIO(response.content)
    image_type = imghdr.what(image_data)
    if image_type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Downloaded file is not a valid image.",
        )

    # Process the image with ALPR
    image_data.seek(0)
    result = alpr.recognize_array(image_data.read())

    return RequestResponse(**result)