"""
Django settings for connect project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['CONNECT_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'debug_toolbar',
    'django_gravatar',
    'connect',
    'accounts',
    'moderation',
    'discover',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'connect.urls'

WSGI_APPLICATION = 'connect.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'connect',
        'USER': 'connect',
        'PASSWORD': os.environ['CONNECT_DB_PASSWORD'],
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Melbourne'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Additional locations of static files
#STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(BASE_DIR, 'static'),
#)

# Media files (user uploaded)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Gravatar Settings

GRAVATAR_DEFAULT_IMAGE = 'retro'


# Site Settings

SITE_ID = 1
SITE_URL = 'http://localhost:8000' #TODO: change for production
# Primary site email address.  Is used as a generic contact point in
# email correspondence
SITE_EMAIL = 'info@connect.test' # TODO: change for production

# Set 'from' email address for system emails

EMAIL_HOST = os.environ['CONNECT_EMAIL_HOST']
EMAIL_PORT = os.environ['CONNECT_EMAIL_PORT']
EMAIL_HOST_USER = os.environ['CONNECT_EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['CONNECT_EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = os.environ['CONNECT_EMAIL_USE_TLS']


AUTH_USER_MODEL = 'accounts.CustomUser'
