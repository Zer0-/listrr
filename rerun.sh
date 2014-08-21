#!/bin/bash

#check inotifywait existance
command -v inotifywait >/dev/null 2>&1 || { echo "inotifywait is not installed.  Aborting." >&2; exit 1; }

source build_static.sh nodo
#cd into directory of this script (assumed to be project root)
SRC_DIR=$DIR
cd $SRC_DIR

STATIC_DIR=$OUT

start_appserver_command="../bin/python listrr"
start_staticserver_command="http-server -p 8888"

#Determine if roxterm is installed on the system - it has nice --tab behaviour
command -v roxterm >/dev/null 2>&1 && ROXTERM=true || ROXTERM=false

function tabbed_start_application_server {
    roxterm --tab -e "bash -c \"cd $SRC_DIR; $start_appserver_command\"" &
}

function tabbed_start_static_server {
    roxterm --tab -e "bash -c \"cd $STATIC_DIR; $start_staticserver_command\"" &
}

function start_application_server {
    if $ROXTERM; then
        tabbed_start_application_server
    else
        cd $SRC_DIR
        $start_appserver_command &
    fi
}

function start_static_server {
    if $ROXTERM; then
        tabbed_start_static_server
    else
        cd $STATIC_DIR
        $start_staticserver_command &
    fi
}

function find_and_kill {
    pid=$(ps ux | grep "$1" | grep -v grep | head -n1 | awk '{print $2}')
    if [ $pid ]; then
        kill $pid
    fi
}

function kill_application_server {
    find_and_kill $start_appserver_command
}

function kill_static_server {
    find_and_kill $start_staticserver_command
}

function buildstatic {
    cd $SRC_DIR
    ./build_static.sh &
}

function killrunning {
    kill_application_server
    kill_static_server
}


function mainloop {
    while true; do
        cd $SRC_DIR
        EVENT=$(inotifywait -q -r -e create -e delete -e modify listrr)
        CHANGED_FILE=$(echo $EVENT | cut -f3 -d " ")
        if [[ $CHANGED_FILE =~ ^.+\.(py$|mako$) ]] || [[ $CHANGED_FILE =~ ^settings.*\.json$ ]]; then
            kill_application_server
            start_application_server
        elif [[ $CHANGED_FILE =~ ^.+\.(scss$|coffee$|css$|js$) ]]; then
            buildstatic
        fi
    done
}

trap killrunning EXIT
start_application_server
start_static_server
buildstatic
mainloop
killrunning #here only if mainloop crashed
