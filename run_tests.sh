#!/bin/bash

export PYTHONPATH=tests:src 
. venv/bin/activate
pip install -r requirements/dev.txt

if [[ "$1" == "watch" ]]
then
   shift
   pytest-watch -- $@
else
   pytest --junitxml=reports/test-report.xml $@
fi
