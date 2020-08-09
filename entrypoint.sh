#!/bin/bash

set -e

echo -e "Running $FLASK_CONFIG Configurations\n*****************\n"

if [ $FLASK_RUN_MIGRATION = 'on' ]; then
  exec flask db upgrade &
fi

if [ $FLASK_CONFIG = 'development' ]; then
  echo -e "Starting development server\n***********\n"
  #exec uwsgi --ini /survey/uwsgi.ini --py-autoreload=1
  exec flask run --host 0.0.0.0
elif [ $FLASK_CONFIG = 'testing' ]; then
  echo -e "Running tests\n************\n"
  exec flask tests
elif [ $FLASK_CONFIG = 'production' ]; then
  echo -e "Starting production server\n************\n"
  exec uwsgi --ini /survey/uwsgi.ini
else
  echo -e "Invalid config $FLASK_CONFIG"
fi
