#!/bin/bash

. $HOME/.venv/bin/activate

num=5
if test "$1" != ""; then
  num=$1
fi

board="$(./g2string.py -f games/test.data)"
rows=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14)

for row in "${rows[@]}"; do
  curl -s -H "Content-Type: application/json" \
    -d '{ "board": "'"$board"'", "letters": "tasje..", "details": 0, "row": '$row' }' \
    http://localhost:8000/ > .row$row &
  echo "sent req $row"
done

wait
cat .row* | sort -n | ./details.py -n $num "$board"
rm -f .row*
