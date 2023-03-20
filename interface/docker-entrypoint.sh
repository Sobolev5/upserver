#!/bin/bash
python manage.py migrate
gunicorn --bind 0.0.0.0:12345 --threads 2 --workers 5 --reload wsgi