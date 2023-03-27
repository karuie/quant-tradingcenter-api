#!/bin/sh

pip install -r requirements.txt
# reference: https://flask.palletsprojects.com/en/2.1.x/deploying/gunicorn/
gunicorn -c gunicorn.conf.py 'main_app:app'
