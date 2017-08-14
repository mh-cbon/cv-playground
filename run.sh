#!/bin/sh

set -x
set -e

script="$1"

if [ "$WW" = "y" ]; then
  rm -fr cwd/* || echo "ok"
  python $script --src "input/" --out "cwd/"
else
  killall main -9 || echo "ok"
  go run web/main.go "cwd/" &
  WW="y" watchrun -care "*.py" sh run.sh $script
fi
