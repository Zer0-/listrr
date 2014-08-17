#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR

function read_setting {
    cat listrr/settings.local.json | \
    python3 -c \
    "import json,sys;js=json.load(sys.stdin);print(js[\"$1\"])"
}
IN=$(read_setting static_buildout_dir)
OUT=$(read_setting served_static_dir)

mkdir $OUT
mkdir $OUT/scss
rm -rfv ./.sass-cache
rm -rv $OUT/scss/*

collect(){
    cd listrr
    ../../bin/python scripts/collectstatic.py
    cd ..
}

build(){
    coffee --compile --output $OUT/coffee $IN/coffee &
    sass --style expanded --update $IN/scss:$OUT/scss
}

collect
build
