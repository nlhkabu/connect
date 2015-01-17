import os
from django.utils.translation import ugettext_lazy as _

"""
Django settings for connect project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('CONNECT_SECRET_KEY',
                            'jj4ie+#b4h=ovjrma7ad*0vhuu8j4fi@8beksc-f+pa_co')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('CONNECT_DEBUG', 'on') == 'on'
TEMPLATE_DEBUG = DEBUG

# Allow all host headers
ALLOWED_HOSTS = os.environ.get('CONNECT_ALLOWED_HOSTS', 'localhost').split(',')


# Application definition

ADMINS = (
    ('Nicole Harris', 'n.harris@kabucreative.com.au'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_behave',
    'django_gravatar',
    'endless_pagination',
    'django_boost',
    'connect',
    'connect_config',
    'accounts',
    'moderation',
    'discover',
)

if DEBUG:
    INSTALLED_APPS += (
        'debug_toolbar',
        'django_extensions',
    )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'connect.urls'

WSGI_APPLICATION = 'connect.wsgi.application'

# Testing
TEST_RUNNER = 'django_behave.runner.DjangoBehaveTestSuiteRunner'

# Pagination
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

ENDLESS_PAGINATION_PREVIOUS_LABEL = '<i class="fa fa-chevron-left"></i>'
ENDLESS_PAGINATION_NEXT_LABEL = '<i class="fa fa-chevron-right"></i>'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Parse database configuration from $DATABASE_URL, if it is set
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['CONNECT_DB_NAME'],
            'USER': os.environ['CONNECT_DB_USER'],
            'PASSWORD': os.environ['CONNECT_DB_PASSWORD'],
            'HOST': os.environ['CONNECT_DB_HOST'],
            'PORT': os.environ['CONNECT_DB_PORT'],
        },
    }


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

USE_I18N = True
USE_L10N = True
USE_TZ = True

TIME_ZONE = 'Australia/Melbourne'
LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = 'static'
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(BASE_DIR, 'static'),
)

# Media files (user uploaded)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Gravatar Settings

GRAVATAR_DEFAULT_IMAGE = 'retro'


# Site Settings

SITE_ID = 1
SITE_URL = 'http://localhost:8000' #TODO: change for production

# Set 'from' email address for system emails

EMAIL_HOST = os.environ['CONNECT_EMAIL_HOST']
EMAIL_PORT = os.environ['CONNECT_EMAIL_PORT']
EMAIL_HOST_USER = os.environ['CONNECT_EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['CONNECT_EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = os.environ['CONNECT_EMAIL_USE_TLS']


# Auth Settings
AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_REDIRECT_URL = '/'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
