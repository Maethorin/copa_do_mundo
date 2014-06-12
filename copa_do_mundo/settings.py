#!/usr/bin/env python
# encoding: utf-8

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

APP_PATH = os.path.join(BASE_DIR)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%zwkr9gs@t2hs)!ce4_j!^&uj!dtsei(5eo75e0k0(*i2@c_9v'

# SECURITY WARNING: don't run with debug turned on in production!
SERVER_TIME_DIFF = 0

ALLOWED_HOSTS = []

CSRF_COOKIE_SECURE = False

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'tabela',
    'south'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'copa_do_mundo.urls'

WSGI_APPLICATION = 'copa_do_mundo.wsgi.application'

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tabela_copa',
        'USER': 'copa',
        'PASSWORD': 'AcopaéN0ssa!',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/


USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(APP_PATH, 'templates'),
)

FACEBOOK_GRAPH_API = "https://graph.facebook.com/v2.0"
FACEBOOK_PAGE_ID = os.environ.get('FACEBOOK_PAGE_ID', None)
FACEBOOK_PAGE_ACCESS_TOKEN = os.environ.get('FACEBOOK_PAGE_ACCESS_TOKEN', None)


#produção
DEBUG = True
LOCAL_DEVELOPMENT = True
TEMPLATE_DEBUG = True
# STATIC_ROOT = '/webapps/copa_do_mundo/app/tabela/static/'
