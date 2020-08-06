# Python 3.7 using Debian 10 (buster)
FROM python:3.7-buster

MAINTAINER Boris Shishov <borisshishov@gmail.com>

# In-container environmental settings
# PLEASE NOTE: THESE VARIABLES ARE USED IN DJANGO SETTINGS MODULE
ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PROJECT_PATH=/opt/cognitive \
    COGNITIVE_MODULES_ROOT=/var/cognitive/modules \
    COGNITIVE_RESULTS_ROOT=/var/cognitive/results \
    DJANGO_STATIC_ROOT=/var/cognitive/static \
    DJANGO_MEDIA_ROOT=/var/cognitive/media \
    PROJECT_LOGS_ROOT=/var/log/cognitive

RUN export DJANGO_SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1) && \
    mkdir -p -v $PROJECT_PATH \
                $COGNITIVE_MODULES_ROOT \
                $COGNITIVE_RESULTS_ROOT \
                $DJANGO_STATIC_ROOT \
                $DJANGO_MEDIA_ROOT \
                $PROJECT_LOGS_ROOT

VOLUME $COGNITIVE_MODULES_ROOT \
       $COGNITIVE_RESULTS_ROOT \
       $DJANGO_STATIC_ROOT \
       $DJANGO_MEDIA_ROOT \
       $PROJECT_LOGS_ROOT

# Copy src files (entrypoint included)
COPY ./src/web $PROJECT_PATH
WORKDIR $PROJECT_PATH

# Requiremens (after src copy)
RUN pip install --no-cache-dir -r $PROJECT_PATH/requirements.txt

# Project port (both for uwsgi setup or for http setup)
EXPOSE $PORT

# Setup the docker entrypoint
# NOTE: It should be with LF (unix) line-endings
COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["help"]
