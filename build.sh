#!/bin/bash

rm -rf tmp
[[ -d tmp ]] && { echo "Please delete tmp folder before build."; exit 1; }
mkdir -p tmp/venv
mkdir -p tmp/package


cp src/* tmp/package/
python3 -m venv tmp/venv
source tmp/venv/bin/activate
pip3 install python-twitter

cp -r tmp/venv/lib/python3.6/site-packages/. tmp/package/
chmod -R 777 tmp
