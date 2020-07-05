#! /bin/bash

media_dir=$(python -c "from configparser import ConfigParser; config = ConfigParser(); config.read('asteria.config'); print(config['Directories']['Media']);")
rm -f ${media_dir}/uploads/*
rm -f announcements/migrations/000*
rm -f challenges/migrations/000*
rm -f teams/migrations/000*
rm -f tests/migrations/000*

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
echo "Creating superuser..."
python manage.py createsuperuser
python manage.py runserver

