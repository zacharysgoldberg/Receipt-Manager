#!/usr/bin/env bash

gunicorn -w 2 --bind :$PORT app:app # 0.0.0.0:5000 
