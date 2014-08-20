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

function get_pid {
    ps ux | grep "$1" | head -n1 | awk '{print $2}'
}

function kill_application_server {
    server_pid=$(get_pid $start_appserver_command)
    kill $server_pid
}

function kill_static_server {
    server_pid=$(get_pid $start_staticserver_command)
    kill $server_pid
}

function buildstatic {
    cd $SRC_DIR
    ./build_static.sh &
}

function killrunning {
    kill_application_server
    kill_static_server
}

command -v roxterm >/dev/null 2>&1 && ROXTERM=true || ROXTERM=false

function mainloop {
    while true; do
        cd $SRC_DIR
        EVENT=$(inotifywait -r -e create -e delete -e modify listrr)
        CHANGED_FILE=$(echo $EVENT | cut -f3 -d " ")
        echo $EVENT
        if [[ $CHANGED_FILE =~ ^.+\.py$ ]]; then
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
#uildstatic
mainloop
#will never get to this if inotify works:
killrunning
