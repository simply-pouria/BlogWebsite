#!/bin/bash
cd ~/BlogWebsite
source /home/PouriaMoradpour/BlogWebsite/venv/bin/activate
git pull origin main
python manage.py migrate
python manage.py collectstatic --noinput
