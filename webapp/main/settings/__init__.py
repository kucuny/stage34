"""
Django settings for stage34 project.

Generated by 'django-admin startproject' using Django 1.9.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

from celery.schedules import crontab
from datetime import timedelta

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
MAIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEBAPP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hpw(&sd(553#b78br%0oo9i*oy+1(g)@3%%v^fw&v+&_!(hmp7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

STAGE34_HOST = 'stage34.io'
STAGE34_PORT = '8000'

# Application definition
INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party
    'debug_toolbar',
    'django_extensions',
]

INSTALLED_APPS += [
    'api.ApiConfig',
    'worker.WorkerConfig'
]

AUTH_USER_MODEL = 'api.User'
AUTHENTICATION_BACKENDS = [
    'api.helpers.backends.JWTAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend'
]

MIDDLEWARE_CLASSES = [
    # 'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'api.helpers.middlewares.JWTAuthenticationMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'
APPEND_SLASH = True

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
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(MAIN_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(WEBAPP_DIR, 'assets/static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(WEBAPP_DIR, 'assets/media')
MEDIA_ADMIN_ROOT = os.path.join(WEBAPP_DIR, 'assets/static/admin')


# Organization
DEFAULT_ORG_NAME = 'stage34'


# JWT
JWT_SECRET = '8hjfdlksah9r74q38opjfdksa'


# Github API Info.
GITHUB_API = {
    'client_id': '7f845815ccbc5c97d622',
    'client_secret': '026219920a2470dbe33af113afe8d781cd154c55',
    'scope': 'user:email,read:org,repo',
    'authorize_url': 'https://github.com/login/oauth/authorize',
    'access_token_url': 'https://github.com/login/oauth/access_token',
    'api_base_url': 'https://api.github.com',
    'redirect_uri': 'http://stage34.io:8000/auth/github/callback/'
}


# Stage Repository
STORAGE_HOME = os.path.join(WEBAPP_DIR, 'storage')


# Docker
DOCKER_COMPOSE_STAGE34_FILE = 'stage34-services.yml'
DOCKER_COMPOSE_TEMP_FILE = 'docker-compose.stage34.yml'
DOCKER_COMPOSE_BIN_PATH = '/usr/local/bin/docker-compose'
DOCKER_BIN_PATH = '/usr/local/bin/docker'


# Host Updater
ETC_HOSTS_UPDATER_PATH = os.path.join(PROJECT_DIR, 'etc', 'scripts', 'host_updater.sh')


# Nginx
NGINX_CONF_PATH = os.path.join(PROJECT_DIR, 'nginx', 'conf.d')
NGINX_BIN_PATH = '/usr/local/bin/nginx'


# Celery Configurations
REDIS_URL = 'redis://0.0.0.0:6379/0'
BROKER_URL = [REDIS_URL]
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_IGNORE_RESULT = False
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 10 * 1     # in seconds
# CELERY_DISABLE_RATE_LIMITS = True
CELERY_ACKS_LATE = False
CELERYD_PREFETCH_MULTIPLIER = 4
CELERYD_MAX_TASKS_PER_CHILD = 10        # pre-forked task pool
CELERYD_CONCURRENCY = 4                 # # of worker processes
CELERY_TIMEZONE = 'Asia/Seoul'
CELERY_ALWAYS_EAGER = False
# TCELERY_RESULT_NOWAIT = False         # tornado celery nowait option
CELERYBEAT_SCHEDULE = {
    'hello-every-10s': {
        'task': 'worker.tasks.hello.say_hello',
        'schedule': timedelta(seconds=10),
        'args': ('world',),
    },
}


try:
    from importlib import import_module
    env = os.environ.get('ENV', 'local')
    custom_conf = import_module('.' + env, __name__)
    for key in filter(lambda x: not x.startswith('__'), dir(custom_conf)):
        globals()[key] = getattr(custom_conf, key)
except (ImportError, AttributeError):
    pass
