#!/bin/bash
set -e
python -m venv venv
. venv/bin/activate
./run_tests.sh
pip install -r requirements/build.txt
python setup.py sdist bdist_wheel