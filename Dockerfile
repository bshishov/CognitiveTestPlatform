# Python 3.4 using Debian Jessie
FROM python:3.4-jessie

MAINTAINER Boris Shishov <borisshishov@gmail.com>

# ALL In-container paths
# PLEASE NOTE: SOME OF THESE PATHS ARE USED IN DJANGO SETTINGS MODULE
ENV PYTHONUNBUFFERED 1
ENV PORT=8000
ENV PROJECT_PATH=/opt/cognitive
ENV PROJECT_USER_DATA=/var/cognitive
ENV COGNITIVE_MODULES_ROOT=$PROJECT_USER_DATA/modules
ENV COGNITIVE_RESULTS_ROOT=$PROJECT_USER_DATA/results
ENV DJANGO_STATIC_ROOT=$PROJECT_USER_DATA/static
ENV DJANGO_MEDIA_ROOT=$PROJECT_USER_DATA/media
ENV PROJECT_LOGS_ROOT=/var/log/cognitive

RUN echo "Image project path: $PROJECT_PATH"
RUN echo "Image user-data path: $PROJECT_USER_DATA"

# Create necessary directories
RUN mkdir $PROJECT_PATH \
    $PROJECT_USER_DATA \
    $COGNITIVE_MODULES_ROOT \
    $COGNITIVE_RESULTS_ROOT \
    $DJANGO_STATIC_ROOT \
    $DJANGO_MEDIA_ROOT \
    $PROJECT_LOGS_ROOT

# Volumes
VOLUME ["$COGNITIVE_MODULES_ROOT", \
        "$COGNITIVE_RESULTS_ROOT", \
        "$DJANGO_STATIC_ROOT", \
        "$DJANGO_MEDIA_ROOT", \
        "$PROJECT_LOGS_ROOT"]

# Copy src files (entrypoint included)
COPY ./src/web $PROJECT_PATH
WORKDIR $PROJECT_PATH

# Upgrade pip and install all required python dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r $PROJECT_PATH/requirements.txt

# Project port (both for uwsgi setup or for http setup)
EXPOSE $PORT

# Setup the docker entrypoint
# NOTE: It should be with LF (unix) line-endings
COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["help"]
