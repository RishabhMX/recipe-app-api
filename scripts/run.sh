#below code to identify as a script file
#!/bin/sh

#fails whole script if even one line fails
set -e

#waits for db to load
python manage.py wait_for_db

#collects all static files and add to script directory
python manage.py collectstatic --noinput

#to make migrations if any
python manage.py migrate


#intializing wsgi server on 9000 port and wsgi workers are 4
#master is main thing running on server
#enable threads to multi-threading
#module app.wsgi to tun wsgi.py in app/app/ folder
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi