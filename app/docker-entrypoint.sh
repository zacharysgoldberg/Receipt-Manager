#!/usr/bin/env bash

# flask db upgrade

gunicorn -w 2 app:app
