#!/bin/bash

NAME="copa_do_mundo"                                  # Name of the application
DJANGODIR=/webapps/copa_do_mundo/app/copa_do_mundo             # Django project directory
SOCKFILE=/webapps/copa_do_mundo/app/run/gunicorn.sock  # we will communicte using this unix socket
USER=copa                                        # the user to run as
GROUP=webapps                                     # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=copa_do_mundo.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=copa_do_mundo.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /usr/local/bin/virtualenvwrapper_lazy.sh
workon copa
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=unix:$SOCKFILE