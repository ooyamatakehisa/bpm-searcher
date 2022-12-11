#! /bin/sh
flask db migrate
flask db upgrade
gunicorn --bind=0.0.0.0:8080 --workers=16 --access-logfile - app:app
