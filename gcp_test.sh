#!/bin/bash

[ -f $HOME/.path.sh ] && . $HOME/.path.sh

num=5
if test "$1" != ""; then
  num=$1
fi

curl -s -H 'Content-Type: application/json' \
  -H "Authorization: bearer $(gcloud auth print-identity-token)" \
  -d '{ "board": "'"$(g2string.py -f games/test.data)"'", "letters": "mjowcyl", "details": '$num' }' \
  https://wordgrid-or5twhev4a-uw.a.run.app

