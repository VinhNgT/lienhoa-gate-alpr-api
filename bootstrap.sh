#!bin/bash

set -e

echo "Compiling OpenALPR..."
cd $OPENALPR_PATH/src
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..
make

echo "Installing OpenALPR..."
sudo make install

echo "Installing Python dependencies..."
cd $WORKSPACE_PATH
pip install --user -r requirements.txt
