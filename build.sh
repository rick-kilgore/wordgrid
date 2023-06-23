#!/bin/zsh

[ -f $HOME/.path.sh ] && source $HOME/.path.sh

realpath=realpath
if test `uname -s` = "Darwin"; then
  realpath=grealpath
fi

startdir=$PWD
rp=$($realpath $0)
dir=$(dirname $rp)
echo "cd $dir/go/"
cd $dir/go
if echo "$0" | grep -q dbuild; then
  echo debug build...
  go build -o ../wordgrid -gcflags='-N -l' . |& sed 's#^\./#./go/#' | tee ../.mk.log
else
  echo release build...
  go build -o ../wordgrid . |& sed 's#^\./#./go/#' | tee ../.mk.log
fi
echo "done -> $($realpath --relative-to=${startdir} ../wordgrid)"

