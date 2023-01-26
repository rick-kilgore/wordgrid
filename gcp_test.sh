#!/bin/bash

. $HOME/.venv/bin/activate

num=5
if test "$1" != ""; then
  num=$1
fi

board="$(g2string.py -f games/test.data)"
rows=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14)
# letters="mjowcyl"
letters="mj.wcy."

# -d '{ "board": "'"$board"'", "letters": "'$letters'", "details": 0 }' \
# -d '{ "board": "'"$board"'", "letters": "'$letters'", "details": 0, "row": '$row' }' \
# -d '{ "board": "'"$board"'", "letters": "'$letters'", "details": 0, "x": '$row', "y": '$col' }' \

row=0
col=0
#for row in "${rows[@]}"; do
  #for col in "${rows[@]}"; do
    curl -s -H 'Content-Type: application/json' \
      -H "Authorization: bearer $(gcloud auth print-identity-token)" \
      -d '{ "board": "'"$board"'", "letters": "'$letters'", "details": 0 }' \
      https://wordgrid-or5twhev4a-uw.a.run.app > .part$row-$col &
    echo "sent req $row-$col"
  #done
#done

wait
cat .part* | sort -n | ./details.py -n $num "$board"
rm -f .part*
