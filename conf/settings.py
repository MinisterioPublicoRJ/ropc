"""
Django settings for conf project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

import dj_database_url
from django.urls import reverse_lazy
from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "simple_history",
    "django_extensions",
]
INTERNAL_APPS = [
    "users",
    "operations",
    "coredata",
    "accounts",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + INTERNAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

GEO_DATABASE_NAME = "geo"
DEFAULT_DATABASE_NAME = "default"
DATABASE_URL = config("DATABASE_URL")
GEO_DATABASE_URL = config("GEO_DATABASE_URL")
DATABASES = {
    DEFAULT_DATABASE_NAME: dj_database_url.parse(DATABASE_URL),
    GEO_DATABASE_NAME: dj_database_url.parse(GEO_DATABASE_URL),
}

DATABASE_ROUTERS = ["conf.db_router.DBRouter"]


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = "users.User"


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = config(
    'STATIC_URL',
    default='/static/'
)
STATIC_ROOT = config(
    'STATIC_ROOT',
    default="/static/"
)
STATICFILES_DIRS = [
    Path(BASE_DIR, "static"),
]

LOGIN_REDIRECT_URL = reverse_lazy("home")
LOGIN_URL = reverse_lazy("login")

OPERATIONS_PER_PAGE = config("OPERATIONS_PER_PAGE", cast=int, default=10)

EMAIL_SMTP_SERVER = config("EMAIL_SMTP_SERVER", default="")
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_DEST_NOTIFY = config("EMAIL_DEST_NOTIFY", cast=Csv(), default="")
EMAIL_SUBJECT = config("EMAIL_SUBJECT", default="")

SKIPPABLE_SECTIONS = (6, 7)

SITE_URL = config("SITE_URL", default="localhost:8888")

TABLEAU_TARGET_SITE = config("TABLEAU_TARGET_SITE")
TABLEAU_WORKBOOK = config("TABLEAU_WORKBOOK")
TABLEAU_VIEW = config("TABLEAU_VIEW")
TABLEAU_HOST = config("TABLEAU_HOST")
TABLEAU_USERNAME = config("TABLEAU_USERNAME")
