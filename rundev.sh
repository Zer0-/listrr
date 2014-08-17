#!/bin/bash

SRC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
STATIC_DIR=/tmp/served_static
GTERM="$(command -v mate-terminal || command -v gnome-terminal)"

cd $SRC_DIR
./build_static.sh

$GTERM\
    --tab -e "bash -c \"cd $STATIC_DIR; pwd; http-server -p 8888\""\
    --tab -e "bash -c \"cd $SRC_DIR; pwd; echo $SRC_DIR; ../bin/python listrr; bash\""

