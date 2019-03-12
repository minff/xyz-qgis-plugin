#!/bin/bash
# python_qgis and test variables like APP_ID needs to be defined in env.sh
shopt -s expand_aliases

[[ "$#" -lt 1 ]] && echo No test python file given.. && exit
py=$1

! [[ -e ./env.sh ]] && echo env.sh is not found && exit
source ./env.sh

testfile=$(echo $py | sed -e 's/\//./g; s/.py//g')
echo Running $testfile ..
python_qgis -m $testfile # treat input as module for valid python import
