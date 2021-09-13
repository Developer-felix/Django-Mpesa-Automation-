##!/bin/sh
#set -e #exit if error occurred
#
#python3 manage.py migrate --no-input
#python3 manage.py collectstatic --no-input
#
#gunicorn config.wsgi:application --bind 127.0.0.1:8080
