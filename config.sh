#!/bin/bash

python manage.py makemigrations visualCancer
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000