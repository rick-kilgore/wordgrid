
if [ -z "$1" -o ! -x ./wordgrid ]; then
  echo "\nUsage: wg <board> [solo [bnum]]"
  echo
  echo "this script should be run from the wordgrid directory\n"
  return
fi

board=$1
shift

specargs="-pb 2"
if [ "$1" == "solo" ]; then
  shift
  bnum=1
  if echo "$1" | grep -Pq '^\d+$'; then
    bnum=$1
    shift
  fi
  specargs="-sb $bnum"
fi

wg() {
  letters=$1; shift
  ./wordgrid -f $board $specargs -w mix.txt $@ $letters te run.clog && vim run.clog mix.txt $board
}

wgs() {
  letters=$1; shift
  ./wordgrid -f $board $specargs -w scrabble_words.txt $@ $letters te run.clog && vim run.clog $board
}

wgl() {
  letters=$1; shift
  ./wordgrid -f $board $specargs -w larger.txt $@ $letters te run.clog && vim run.clog $board
}

bd() {
  PS1="${PS1/ \(\[1;31mwg *\[m\)/}"
  . ./wgsetup.sh "$1"
  vim "$1"
}

PS1="${PS1/:/ ([1;31mwg $board[m):}"

destroy() {
  unfunction wg wgs wgl bd destroy
  PS1="${PS1/ \(\[1;31mwg *\[m\)/}"
  wg() {
    . ./wgsetup.sh
  }
}
