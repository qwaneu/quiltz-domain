#!/bin/bash
plantuml -tsvg README.md
mv *.svg doc/images/
