#!/bin/bash

num=5
if test "$1" != ""; then
  num=$1
fi

curl -s -H "Content-Type: application/json" \
  -d '{ "board": "'"$(g2string.py -f games/test.data)"'", "letters": "mjowcyl", "details": '$num' }' \
  http://localhost:8000/
