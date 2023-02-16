#!/bin/zsh

[ -f $HOME/.path.sh ] && source $HOME/.path.sh

if test "$1" = "-d"; then
  go build -gcflags=all='-N -l' . |& tee mk.log
else
  go build . |& tee mk.log
fi

