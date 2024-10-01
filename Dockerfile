FROM python:3.12-bullseye

RUN apt-get update && apt-get install -y libopencv-dev libtesseract-dev git cmake build-essential \
    libleptonica-dev liblog4cplus-dev libcurl3-dev

COPY ./openalpr /code/openalpr
WORKDIR /code/openalpr/src/build
RUN cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc .. \
    && make && make install

WORKDIR /code
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./fastapi_app /code/fastapi_app
CMD ["fastapi", "run", "fastapi_app/main.py", "--port", "80"]
