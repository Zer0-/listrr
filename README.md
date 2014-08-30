listrr
======

Simple nested task list built with [Bricks](https://github.com/Zer0-/bricks.git)

[Live Site / Demo](http://listrr.frontalgaming.com/)

Users may create semi-private lists - lists are created with a url that's impossible to guess so only
anyone that knows the url will see your list.

A handy feature of listrr is that each item in the list has it's own url. It's possible to make a nested list
and share the url of only one sub-list without worrying about anyone seeing the rest of your list.
This could be useful for collaboration since you can see when others have checked off items in the list.

Tested only under python3.4


Installation
=========

### Prerequisites
Requires [Sass](http://sass-lang.com/) and [Coffeescript](http://coffeescript.org/).

Requires a Postgres database.

listrr uses psycopg2 to connect to Postgres which may have some prerequisites, under Ubuntu you might need to do

`sudo apt-get install libpq-dev python-dev`


### Repository
create a virtual env

```
pyvenv listrr_environment
cd listrr_environment
```

clone the repo

```
git clone https://github.com/Zer0-/bricks.git
cd bricks
```

initialize the submodules

```
git submodule init
git submodule update
```

run the setup

`../bin/python setup.py develop`


### Settings
You will notice a settings.json file in the listrr source directory. You should edit this file
to fill in your settings or preferrably copy it to a file named settings.local.json since it will override settings.json
and not be tracked by git.

(Note: there's a bit of a bug right now in the order of which Bricks [the library listrr depends on] looks for settings.
It will try to use the settings.json file in the main module's directory before checking the current working directory for settings.local.json so at the moment it's best to leave the settings.local.json file in the listrr source directory (listrr/listrr))

listrr checks the main module's directory (in this case the source directory listrr/listrr) or the current working directory for settings files settings.local.json or settings.json. In that order.

`list_uuid_size` affects the size of the generated url. A value between 5 and 10 is sane. Any lower is secure
and any higher will yield needlessly long urls.

listrr has some static assets built with Coffeescript and Sass as well as ordinary javascript. The setting `served_static_dir` should be the location you are serving these static files from and `static_buildout_dir` is where the script collectstatic.py (in the scripts subdirectory)
will move any static assets that need to be compiled.

listrr is not responsible for serving static assets. It assumes there is a server that is serving them on the url under the setting
`served_static_url`.
(`python3 -m http.server 8888` will serve the current directory on port 8888. This will do just fine as a static server during development). More on this in a bit.

###Running listrr

Double checking that your database settings are correct we will need to initialize the db schema:

Assuming you are in the virtualenv directory, run

`./bin/python listrr/listrr/scripts/initdb.py`

We can then run the actual application:

`./bin/python listrr/listrr`

And it should happily run.

###Scripts
There is a handy script in the root of the project folder called rerun.sh. It handles the task of running the collectstatic.py
script, running sass and coffee to build the static files and launches a static server to serve them. It also monitors
the project directory for changes and either restarts the server or rebuilds the files accordingly.

rerun.sh uses inotify-tools to monitor files for changes so make sure this is installed. It also uses node's http-server to serve
static files (there's no good reason for this but you can install it with `npm install -g http-server`). If you have roxterm installed
it will run each server or build process in a separate tab.

Kill the server (Ctrl+C) and try it out with `./rerun.sh`


Footer
=========

Feel free to hit me at phil.volguine@gmail.com for help.


My next project is to document Bricks which is a web framework I created and what listrr uses for routing and other things.
So for now everyone is unfortunately stuck code spelunking.
