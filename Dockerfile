FROM python:3.12-bullseye

# Install OpenALPR dependencies
RUN apt-get update && apt-get install -y libopencv-dev libtesseract-dev git  \
    cmake build-essential libleptonica-dev liblog4cplus-dev libcurl3-dev

# Compile and install OpenALPR
COPY ./openalpr /code/openalpr
WORKDIR /code/openalpr/src/build
RUN cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr \
    -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc .. && make && make install

# Install Python dependencies
WORKDIR /code
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Start the FastAPI server
COPY ./fastapi_app /code/fastapi_app
COPY ./version.txt /code/version.txt
CMD ["fastapi", "run", "fastapi_app/main.py", "--port", "80"]
