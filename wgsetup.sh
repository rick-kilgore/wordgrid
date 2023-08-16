
if [ -z "$1" -o ! -x ./wordgrid ]; then
  echo "\nUsage: wg <board> [solo [bnum]]"
  echo
  echo "this script should be run from the wordgrid directory\n"
  return
fi

solo=0
board=$1
if [ ! -f $board ]; then
  if echo $board | grep -q games/; then
    cp blank.data $board
  else
    solo=1
    cp solo.data $board
  fi
fi
shift

specargs="-pb 2"
if [ "$1" == "solo" ]; then
  solo=1
  bnum=1
  shift
elif echo $board | grep -qv games/; then
  solo=1
  bnum=1
fi
if [ "$solo" -gt 0 ]; then
  if echo "$1" | grep -Pq '^\d+$'; then
    bnum=$1
    shift
  fi
  specargs="-sb $bnum"
elif echo "$1" | grep -Pq '^\d+$'; then
  specargs="-pb $1"
  shift
fi

wg() {
  letters=$1; shift
  ./wordgrid -f $board $specargs -w mix.txt $@ $letters te run.clog && vim run.clog mix.txt $board
}

wgs() {
  letters=$1; shift
  ./wordgrid -f $board $specargs -w scrabble_words.txt $@ $letters te run.clog && vim run.clog scrabble_words.txt $board
}

wgl() {
  letters=$1; shift
  ./wordgrid -f $board $specargs -w larger.txt $@ $letters te run.clog && vim run.clog larger.txt $board
}

bd() {
  PROMPT="${PROMPT/ \(\%\{*31m\%\}*:/:}"
  . ./wgsetup.sh $@
}

PROMPT="${PROMPT/: /} (%{[1;31m%}wg ${board}%{[m%}): "

destroy() {
  unfunction wg wgs wgl bd destroy
  PROMPT="${PROMPT/ \(\%\{*31m\%\}*:/:}"
  wg() {
    . ./wgsetup.sh
  }
}

vim $board
