#!/bin/bash

ROOTDIR=/scratch2/www/writersinthecloud/

. /scratch2/www/writersinthecloud/witc_env/bin/activate

#python3 manage.py runserver 3039
uwsgi --virtualenv $VIRTUAL_ENV --socket 127.0.0.1:3040 --chdir $ROOTDIR --wsgi-file $ROOTDIR/wsgi.py --logto $ROOTDIR/witc.uwsgi.log --log-date --log-5xx --master --processes 4 --threads 2 --need-app --pidfile ./witc.pid --py-autoreload 1
