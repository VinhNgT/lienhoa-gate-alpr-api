#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")"

cd "../ultimateALPR-SDK/binaries/linux/x86_64"
export PYTHONPATH=$PYTHONPATH:.:../../../python
export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH

python ../../../samples/python/recognizer/recognizer.py --image ../../../assets/images/lic_us_1280x720.jpg --assets ../../../assets --openvino_enabled True
