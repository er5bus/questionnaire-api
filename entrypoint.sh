#!/bin/bash

set -e

echo -e "Running $FLASK_CONFIG Configurations\n*****************\n"

if [[ $FLASK_RUN_MIGRATION = "on" ]]; then
  echo -e "Wait for database to start : Waiting \n"
  exec sleep 10 &
  wait $!
  echo -e "Run migrations : Start \n"
  exec flask db upgrade &
  wait $!
  echo -e "Run migrations : Done \n"
fi

if [[ $FLASK_CREATE_ROOT = "on" ]]; then
  echo -e "Create root user : Start \n"
  exec flask create_admin $ROOT_USERNAME $ROOT_PASSWORD &
  wait $!
  echo -e "Create root user : Done \n"
fi

if [[ $FLASK_CONFIG = "development" ]]; then
  echo -e "Starting development server\n***********\n"
  exec uwsgi --ini /survey/uwsgi.ini --py-autoreload=1 --cheaper=N
elif [[ $FLASK_CONFIG = "testing" ]]; then
  echo -e "Running tests\n************\n"
  exec flask tests
elif [[ $FLASK_CONFIG = "production" ]]; then
  echo -e "Starting production server\n************\n"
  exec uwsgi --ini /survey/uwsgi.ini
else
  echo -e "Invalid config $FLASK_CONFIG"
fi
