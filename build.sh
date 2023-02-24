#!/bin/zsh

[ -f $HOME/.path.sh ] && source $HOME/.path.sh

startdir=$PWD
rp=$(realpath $0)
dir=$(dirname $rp)
echo "cd $dir/go/"
cd $dir/go
if echo "$0" | grep -q dbuild; then
  echo debug build...
  go build -o ../wordgrid -gcflags='-N -l' . |& tee mk.log
else
  echo release build...
  go build -o ../wordgrid . |& tee mk.log
fi
echo "done -> $(realpath --relative-to=${startdir} ../wordgrid)"

