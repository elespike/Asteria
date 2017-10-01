#! /bin/bash

media_dir=$(python -c "from configparser import ConfigParser; config = ConfigParser(); config.read('asteria.config'); print(config['Directories']['Media']);")
rm ${media_dir}/uploads/*
exit 0
rm announcements/migrations/000*
rm challenges/migrations/000*
rm teams/migrations/000*
rm tests/migrations/000*

db_name=$(python -c "from configparser import ConfigParser; config = ConfigParser(); config.read('asteria.config'); print(config['Database']['Name']);")
if [[ -f ${db_name} ]]
then
    rm ${db_name}
else
    echo "drop database ${db_name}; create database ${db_name};" | python manage.py dbshell
fi

python manage.py makemigrations
python manage.py migrate
python manage.py create_test_data
python manage.py createsuperuser
python manage.py runserver

