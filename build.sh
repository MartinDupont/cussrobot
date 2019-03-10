#!/bin/bash

rm -rf tmp
[[ -d tmp ]] && { echo "Please delete tmp folder before build."; exit 1; }
mkdir -p tmp/package


cp src/* tmp/
pip3 install python-twitter --target tmp

chmod -R 777 tmp
