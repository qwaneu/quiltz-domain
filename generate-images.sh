#!/bin/bash
plantuml -tsvg README.md
plantuml -tsvg doc/index.md
mv *.svg doc/images/
mv doc/*.svg doc/images/
