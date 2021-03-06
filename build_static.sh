#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


function read_setting {
    cat $DIR/listrr/settings.local.json | \
    python3 -c \
    "import json,sys;js=json.load(sys.stdin);print(js[\"$1\"])"
}
IN=$(read_setting static_buildout_dir)
OUT=$(read_setting served_static_dir)

collect(){
    cd listrr
    ../../bin/python scripts/collectstatic.py
    cd ..
}

build(){
    coffee --compile --output $OUT/coffee $IN/coffee &
    sass --style expanded --update $IN/scss:$OUT/scss
}

if [ -z "$1" ]; then
    cd $DIR
    mkdir $OUT
    mkdir $OUT/scss
    rm -rf ./.sass-cache
    rm -rv $OUT/scss/*
    collect
    build
fi

