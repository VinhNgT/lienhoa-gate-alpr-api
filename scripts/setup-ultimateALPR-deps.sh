#!/bin/bash

cd $LD_LIBRARY_PATH

echo "Building ultimateALPR Python extension..."
if [ ! -f _ultimateAlprSdk.so ]; then
    python ../../../python/setup.py build_ext --inplace -v
else
    echo "ultimateALPR Python extension already built."
fi

echo "Downloading librensorflow..."
if [ ! -f libtensorflow.so ]; then
    wget https://doubango.org/deep_learning/libtensorflow_r1.14_cpu_linux_x86-64.tar.gz
    tar -xvf libtensorflow_r1.14_cpu_linux_x86-64.tar.gz
    rm libtensorflow_r1.14_cpu_linux_x86-64.tar.gz
else
    echo "librensorflow already downloaded."
fi
