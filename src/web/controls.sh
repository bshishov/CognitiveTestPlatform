#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo 'DIR: ${DIR}'

function start {
    echo 'starting server'
    uwsgi --ini ${DIR}/uwsgi.ini --chdir ${DIR}
}

function stop {
    echo 'stopping server'
    if [ ! -f /var/run/cognitive-django/uwsgi.pid ]; then
        uwsgi --stop /var/run/cognitive-django/uwsgi.pid
    else
        echo 'uwsgi pidfile not found'
    fi
}

case "$1" in
"start")
    start
;;

'stop')
    stop
;;

'restart')
    stop
    sleep 3
    start
;;

'reload')
    touch /var/run/cognitive-django/uwsgi-touch
;;

*)
    echo "use (start|stop|restart|reload) to manage server"
esac

exit 0