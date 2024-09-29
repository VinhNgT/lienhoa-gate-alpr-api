#!/bin/bash

cd ultimateALPR-SDK/binaries/linux/x86_64

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

echo "Installing Intel oneAPI runtime libs..."
if ! dpkg -l | grep -q intel-oneapi-runtime-dpcpp-cpp; then
    # download the key to system keyring
    wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB |
        gpg --dearmor | sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg >/dev/null

    # add signed entry to apt sources and configure the APT client to use Intel repository:
    echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list

    sudo apt update
    sudo apt install intel-oneapi-runtime-dpcpp-cpp -y
else
    echo "Intel oneAPI runtime libs already installed."
fi

echo "Setting permissions..."
chmod +x benchmark
