#!/bin/bash

echo "Installing OpenALPR prerequisites..."

sudo apt update
sudo apt install -y libopencv-dev libtesseract-dev git cmake build-essential \
    libleptonica-dev liblog4cplus-dev libcurl3-dev
