import imghdr
import os
from contextlib import asynccontextmanager
from io import BytesIO

import requests
from fake_useragent import UserAgent
from fastapi import FastAPI, HTTPException, UploadFile, status
from fastapi.responses import PlainTextResponse

from fastapi_app.models import RequestResponse
from openalpr import Alpr

alpr = Alpr("vn", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
ua = UserAgent()

# Get the app's version number.
try:
    with open("version.txt", "r") as version_file:
        VERSION = version_file.read().strip()

except FileNotFoundError:
    VERSION = "0.0.1"

# The number of results to return for each image.
ALPR_TOP_N = os.getenv("ALPR_TOP_N")
if ALPR_TOP_N is not None:
    ALPR_TOP_N = int(ALPR_TOP_N)
    print(f"Setting top-n to {ALPR_TOP_N}")
    alpr.set_top_n(ALPR_TOP_N)

# See openalpr/runtime_data/postprocess/vn.patterns for available patterns.
DEFAULT_PATTERN = os.getenv("DEFAULT_PATTERN")
if DEFAULT_PATTERN:
    print(f"Setting default-pattern (default-region) to {DEFAULT_PATTERN}")
    alpr.set_default_region(DEFAULT_PATTERN)

# The prewarp configuration. Run openalpr-utils-calibrate {image_path} to get
# this value.
PREWARP = os.getenv("PREWARP")
if PREWARP:
    print(f"Setting pre-warp to {PREWARP}")
    alpr.set_prewarp(PREWARP)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if alpr.is_loaded():
        alpr.unload()


app = FastAPI(
    title="LienHoa auto gate - ALPR API",
    version=VERSION,
    summary="API xử lý nhận diện biển số xe.",
    contact={
        "name": "Nguyễn Thế Vinh",
        "url": "https://github.com/VinhNgT",
        "email": "victorpublic0000@gmail.com",
    },
    lifespan=lifespan,
)


@app.get(
    "/",
    summary="Welcome screen",
    tags=["pages"],
    response_class=PlainTextResponse,
)
def homescreen():
    return "Hello, World!"


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
