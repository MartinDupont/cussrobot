#!/bin/bash

rm -rf tmp
[[ -d tmp ]] && { echo "Please delete tmp folder before build."; exit 1; }
mkdir -p tmp/venv
mkdir -p tmp/package


cp src/ tmp/package/
python3 -m venv tmp/venv
source tmp/venv/bin/activate
pip3 install -r python-twitter



chmod -R 777 tmp
