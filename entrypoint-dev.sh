#!/usr/bin/env sh
sleep 1
python manage.py makemigrations staff
python manage.py makemigrations inventory
python manage.py migrate
sleep 1
python DJANGO_DEBUG=1 manage.py runserver 0.0.0.0:8000
