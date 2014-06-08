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
DEBUG = True
LOCAL_DEVELOPMENT = True
TEMPLATE_DEBUG = True
SERVER_TIME_DIFF = 0

ALLOWED_HOSTS = []

CSRF_COOKIE_SECURE = False

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
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

URL_BASE_DE_RESULTADOS = "http://globoesporte.globo.com/servico/esportes_campeonato/widget-uuid/c36d99dd-918a-459f-bf0c-648dec5773af/fases"
URL_RESULTADOS_DE_CLASSIFICACAO = "/fase-grupos-copa-do-mundo-2014/grupo/{}/rodada/{}/jogos.html"
URL_RESULTADOS_DE_MATA_MATA = "/oitavas-copa-do-mundo-2014/classsificacao.html"
URL_DE_GRUPOS = {
    "A": "1069",
    "B": "1070",
    "C": "1071",
    "D": "1072",
    "E": "1073",
    "F": "1074",
    "G": "1075",
    "H": "1166",
}
