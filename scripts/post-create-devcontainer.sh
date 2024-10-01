#!/bin/bash

echo "Installing OpenALPR prerequisites..."
sudo apt update
sudo apt install -y libopencv-dev libtesseract-dev git cmake build-essential \
    libleptonica-dev liblog4cplus-dev libcurl3-dev

echo "Compiling OpenALPR..."
cd $OPENALPR_PATH/src
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..
make

echo "Installing OpenALPR..."
sudo make install

# echo "Creating Python virtual environment for easier go to definition..."
# cd $WORKSPACE_PATH
# python -m venv .venv
# source .venv/bin/activate

# echo "Installing OpenALPR Python bindings..."
# cd $OPENALPR_PATH/src/bindings/python
# python setup.py install --user

echo "Installing Python dependencies..."
cd $WORKSPACE_PATH
pip install --user -r requirements.txt
