#!/bin/bash
set -e
python -m venv venv
./run_tests.sh
pip install -r requirements/build.txt
pip list
ls /opt/hostedtoolcache/Python/3.8.15/x64/lib/python3.8/site-packages/
python setup.py sdist bdist_wheel