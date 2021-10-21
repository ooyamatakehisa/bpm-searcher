#! /bin/sh
flask db migrate
flask db upgrade
python3 -m flask run --host=0.0.0.0 --port=8000
