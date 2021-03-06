"""
For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import dj_database_url

# Global debug switch
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ['true', '1', 'yes']
THUMBNAIL_DEBUG = DEBUG

# [REQUIRED] The secret key to generate tokens
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# [REQUIRED] A path where all of the modules with tests should be located (downloaded)
TESTS_MODULES_DIR = os.environ['COGNITIVE_MODULES_ROOT']

# [REQUIRED] A path where all of the result files will be places
TESTS_RESULTS_DIR = os.environ['COGNITIVE_RESULTS_ROOT']

# Local only (must be proxied with nginx or similar)
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# DJANGO_HOST specifies additional hosts for django, comma separated
additional_hosts = os.environ.get('DJANGO_HOST', None)
if additional_hosts is not None:
    ALLOWED_HOSTS += list(map(str.strip, additional_hosts.split(',')))

""" Database connection is specified by url from env:
Examples:
    postgres://USER:PASSWORD@HOST:PORT/NAME
    mysql://USER:PASSWORD@HOST:PORT/NAME
    sqlite:////full/path/to/your/database/file.sqlite
"""
DATABASES = {
    'default': dj_database_url.config('DJANGO_DB_URL',
                                      default='sqlite:///cognitive.sqlite',
                                      conn_max_age=int(os.environ.get('DJANGO_DB_CONN_MAX_AGE', '600')))
}


# Application definition
INSTALLED_APPS = [
    'cognitive_tests',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # additional
    'rest_framework',
    'django_ace',
    'pagedown',
    'markdown_deux',
    'django_cleanup',
    'sortedm2m',
    'sorl.thumbnail',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cognitive_tests.views.context_processor',
            ],
        },
    },
]

# added to fix template first string being empty
# FILE_CHARSET = 'utf-8-sig'
WSGI_APPLICATION = 'web.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = os.environ.get('DJANGO_LANGUAGE_CODE', 'ru-RU')
TIME_ZONE = os.environ.get('DJANGO_TIME_ZONE', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.environ['DJANGO_STATIC_ROOT']

# Media files (cover images, avatars...)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ['DJANGO_MEDIA_ROOT']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': u'%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': u'%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        }
    },
}

# PATCH LOGGING UNICODE
import logging
logging._defaultFormatter = logging.Formatter(u"%(message)s")
