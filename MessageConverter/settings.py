"""
Django settings for MessageConverter project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@vrs@#www%=p!#pc-1h19g_((r5a6cdw5-gh*73puq-$4ejyjh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'message_converter',
    'south',
    'djcelery',
    'django_extensions',
    'raven',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'MessageConverter.urls'

WSGI_APPLICATION = 'MessageConverter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'message_converter',
        'USER': 'postgres',                                 # Not used with sqlite3.
        'PASSWORD': '',                                     # Not used with sqlite3.
        'HOST': '',                                         # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                         # Set to empty string for default. Not used with sqlite3.
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
BROKER_URL = "redis://localhost:6379/0"
CELERYBEAT_SCHEDULER="djcelery.schedulers.DatabaseScheduler"



#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


SENTRY_DSN = "http://74ef9a98f96141779f63ceb213aed0c9:2902b3c9b54c48efac68b63fab839c57@test.againfaster.com:9000/5"

RAVEN_CONFIG = {
    'dsn' : SENTRY_DSN,
    'register_signals': True,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
        },
    'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s [ %(module)s %(lineno)d ] %(process)d %(thread)d %(message)s'
            },
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
    'handlers': {
        'sentry': {
            'level': 'DEBUG',
            'class': 'raven.contrib.django.handlers.SentryHandler',
            'formatter' : 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'celery_log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/logs/againfaster_celery.log' % PROJECT_PATH,
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        # '': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': True
        # },
        # 'default': {
        #     'level': 'INFO',
        #     'handlers': ['console'],
        #     'propagate': False,
        # },
        # 'django.db': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        #     'propagate': False,
        #     },
        # 'django.db.backends': {
        #     'level': 'ERROR',
        #     'handlers': ['sentry', 'console'],
        #     'propagate': False,
        # },
        'message_converter.tasks': {
           'level': 'INFO',
            'handlers': ['console', 'celery_log_file'],
            'propagate': False,
        },
        # 'raven': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        #     'propagate': False,
        #     },
        # 'sentry.errors': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        #     'propagate': False,
        #     },
        # 'filer' : {
        #     'handlers': ['console'],
        #     'level': 'INFO',
        #     'propagate': True
        # },
    },
}


REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}

FTP_USER = ''
FTP_PASSWD = ''
FTP_HOST = ''

# Load the local settings file
try:
    from MessageConverter.local_settings import *
except ImportError:
    pass
