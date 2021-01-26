"""
Django settings for LostEmpire project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

import os
import dotenv
import django_heroku
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# Load all the enviroment values if running on local machine
# Use local Database (This is because of Heroku having it's own)
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# SECURITY WARNING: keep the secret key used in production secret!
if os.getenv("SECRET_KEY"):
    SECRET_KEY = os.getenv("SECRET_KEY")
else:
    SECRET_KEY = '8cf&qfei&ux!k%43vjyfo^xp0l6ao^axa5wqirng^_@gq06(lx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "127.0.0.1",
    "192.168.100.2",
    "lostempire.herokuapp.com"
    ]

ADMINS = [("LT.Sana", "snm.developer@gmail.com")]

MANAGERS = [("LT.Sana", "snm.developer@gmail.com")]

# Cloudinary Credentials
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}

# Application definition

INSTALLED_APPS = [
    'App0.apps.App0Config', # Tell Django to look at App0
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LostEmpire.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'LostEmpire.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Set to use Heroku's Database if available
# if Heroku Database is not available use local Database if available
DATABASES = {}
DATABASES["default"] = dj_database_url.config(conn_max_age=600)

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}


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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
PROJECT_ROOT = "staticfiles"
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# This is the static files folder name which you created in django project root folder.
# This is different from above STATIC_URL. 
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

#  Add configuration for static files storage using whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Redirect users to login page if they aren't logged in and trying to access a part that requires Authentication
LOGIN_URL = "/signin"

#
# Google Drive Storage Settings
#

GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = None
#GOOGLE_DRIVE_STORAGE_MEDIA_ROOT = MEDIA_ROOT

# reCAPTCHA v3
RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

# Email settings
#EMAIL_HOST = 'smtp.sendgrid.net'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
#EMAIL_HOST_USER = 'apikey'
#EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')

# The FROM email address
#MAIL_SENDER = os.getenv("MAIL_SENDER") # The email address FROM

# Get credentials for PayPal
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")

# Change Django's Default Email From
#DEFAULT_FROM_MAIL = "Lost Empire <noreply@lostempire.herokuapp.com>"

# Set this to True to avoid transmitting the CSRF cookie over HTTP accidentally.
CSRF_COOKIE_SECURE = True

# Set this to True to avoid transmitting the session cookie over HTTP accidentally.
SESSION_COOKIE_SECURE = True

# Enabling persistent database connections can result in a nice speed-up when connecting to 
# the database accounts for a significant part of the request processing time.
CONN_MAX_AGE = 500 # Integer is seconds (60 - seconds, 1 - second and so on)

# To always redirect the user to HTTPS
SECURE_SSL_REDIRECT = True

# *** WARNING ***
# DO NOT CHANGE THIS VALUE FROM 60s
# IF SET TO LONGER IT WILL BREAK YOUR SITE IF HTTPS CONNECTION IS LOST
SECURE_HSTS_SECONDS = 60

# Cloudinary Settings for File Upload Storage
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
