#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo 'DIR: ${DIR}'

function start {
    echo 'starting server'
    uwsgi --ini ${DIR}/uwsgi.ini --chdir ${DIR}
}

function stop {
    echo 'stopping server'
    uwsgi --stop /var/run/cognitive-django/uwsgi.pid
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