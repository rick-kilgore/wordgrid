#!/bin/bash

num=5
if test "$1" != ""; then
  num=$1
fi

curl -s -H "Content-Type: application/json" \
  -d '{ "board": 0, "file": "games/test.data", "letters": "mjowcyl", "details": '$num' }' \
  http://localhost:8000/
