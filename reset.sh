#! /bin/bash

rm db.sqlite3
rm announcements/migrations/000*
rm challenges/migrations/000*
rm teams/migrations/000*
rm settings/migrations/000*
rm media/uploads/*
python manage.py makemigrations
python manage.py migrate
python manage.py populate_test_data
python manage.py createsuperuser
python manage.py runserver 10.0.2.15:8000

