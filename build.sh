#!/bin/bash
set -e
python -m venv venv
./run_tests.sh
pip install -r requirements/build.txt
pip list
python setup.py sdist bdist_wheel