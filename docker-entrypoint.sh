#!/usr/bin/env bash
set -e

echo "CognitiveTestPlatform ENTRYPOINT. PROJECT_PATH=$PROJECT_PATH";

case "$1" in
    "debug")
        shift;
        python manage.py migrate
        python manage.py collectstatic --noinput

        echo "Running Django server on port ${PORT:-8000}"
        exec python manage.py runserver 0.0.0.0:${PORT:-8000} "$@"
    ;;
    "run")
        shift;
        python manage.py migrate
        python manage.py collectstatic --noinput

        echo "Running Gunicorn on port ${PORT:-8000}"
        exec gunicorn web.wsgi:application \
         --name cognitive \
         --bind 0.0.0.0:${PORT:-8000} \
         --workers 3 \
         --log-level=info \
         --log-file=${PROJECT_LOGS_ROOT}/gunicorn.log \
         --access-logfile=${PROJECT_LOGS_ROOT}/access.log \
         "$@"
    ;;
    "manage")
        # All python manage.py operations
        shift;
        exec python manage.py "$@";
    ;;
    *)
        echo "Usage: (run|debug|manage) to manage server"
        echo "    run - runs the gunicorn UWSGI server"
        echo "    debug - runs the django web server"
        echo "    manage [args] - redirect commands to manage.py"
        exit 0;
    ;;
esac

exec "$@"