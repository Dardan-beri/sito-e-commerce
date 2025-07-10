#!/bin/bash

#install dependecies
pip install setuptools
pip install -r requirements.txt

#run django commands
python manage.py makemigrations
python manage.pymigrate
python manage.py tailwind install
python manage.py collectstatic
python manage.py tailwind start