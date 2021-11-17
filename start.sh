# nohup gunicorn -w 8 -b 0.0.0.0:1919 app:server

gunicorn -c gunicorn.conf app:server
##
# ps -ef|grep gunicorn|grep -v grep|cut -c 9-15|xargs kill -9