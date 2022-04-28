#!/usr/bin/env bash

# flask db upgrade

gunicorn --bind 0.0.0.0:8000 -w 2 app:app
