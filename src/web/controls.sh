#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo 'DIR: ${DIR}'

case "$1" in
"start")
echo 'starting server'
uwsgi --ini ${DIR}/uwsgi.ini
;;

'stop')
echo 'stopping server'
uwsgi --stop /var/run/cognitive-django/uwsgi.pid
;;

'restart')
sh ./server.sh stop
sleep 3
sh ./server.sh start
;;

'reload')
touch /var/run/cognitive-django/uwsgi-touch
;;
*)

echo "use (start|stop|restart|reload) to manage server"
esac
exit 0