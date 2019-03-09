#!/bin/bash
set -ex

yum -y update
yum -y install python37 python37-devel python37-pip wget tar gzip cmake gcc-c++ make openssl-devel python3-devel \
 libffi-devel libssh2-devel
yum -y install awscli

rm -rf tmp
[[ -d tmp ]] && { echo "Please delete tmp folder before build."; exit 1; }
mkdir -p tmp/venv
mkdir -p tmp/ackage


# Build deployment-hook
cp deployment-hook-lambda/setup.py tmp/deployment-hook/package/
cp deployment-hook-lambda/requirements.txt tmp/deployment-hook/package/
cp -r deployment-hook-lambda/deploymenthook tmp/deployment-hook/package/
python3 -m venv tmp/deployment-hook/venv
source tmp/deployment-hook/venv/bin/activate
pushd tmp
export LIBGIT2=$VIRTUAL_ENV
wget https://github.com/libgit2/libgit2/archive/v0.27.0.tar.gz
tar xzf v0.27.0.tar.gz
pushd libgit2-0.27.0
cmake . -DCMAKE_INSTALL_PREFIX=$LIBGIT2 -DENABLE_REPRODUCIBLE_BUILDS=ON -DCMAKE_BUILD_TYPE=Release
make
make install
popd
popd
export LDFLAGS="-Wl,-rpath='$LIBGIT2/lib',--enable-new-dtags"
pip3 install -r deployment-hook-lambda/requirements.txt
cp -r tmp/deployment-hook/venv/lib/python3.7/site-packages/. tmp/deployment-hook/package/
cp tmp/deployment-hook/venv/lib/libgit2.so.27 tmp/deployment-hook/package/
pip3 install pytest
pushd deployment-hook-lambda
rm -rf .pytest_cache ./**/__pycache__
python3 -m pytest
rm -rf .pytest_cache ./**/__pycache__
popd

# Build generate-deployment-credentials
cp generate-deployment-credentials-lambda/setup.py tmp/generate-deployment-credentials/package/
cp generate-deployment-credentials-lambda/requirements.txt tmp/generate-deployment-credentials/package/
cp -r generate-deployment-credentials-lambda/credentials tmp/generate-deployment-credentials/package/
python3 -m venv tmp/generate-deployment-credentials/venv
source tmp/generate-deployment-credentials/venv/bin/activate
pip3 install -r generate-deployment-credentials-lambda/requirements.txt
cp -r tmp/generate-deployment-credentials/venv/lib/python3.7/site-packages/. tmp/generate-deployment-credentials/package/
pip3 install pytest
pushd generate-deployment-credentials-lambda
rm -rf .pytest_cache ./**/__pycache__
python3 -m pytest
rm -rf .pytest_cache ./**/__pycache__
popd

chmod -R 777 tmp
