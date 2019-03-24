#!/bin/bash

rm -rf tmp
[[ -d tmp ]] && { echo "Please delete tmp folder before build."; exit 1; }
mkdir -p tmp/package

pip3 install pandas
python3 setup/make_processed_database.py

cp src/* tmp/
pip3 install numpy python-twitter --target tmp

ls tmp
chmod -R 777 tmp
