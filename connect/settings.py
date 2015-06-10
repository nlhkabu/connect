import os
import cbs
import dj_database_url
from cbs import BaseSettings as DefaultSettings
from django.utils.translation import ugettext_lazy as _


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class BaseSettings(DefaultSettings):
    # REQUIRED FOR DJANGO CLASSY SETTINGS
    PROJECT_NAME = 'connect'

    # DEBUG
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = False

    # SITE CONFIGURATION
    SITE_ID = 1

    ADMINS = (
        ('Nicole Harris', 'n.harris@kabucreative.com.au'),
    )

    ROOT_URLCONF = 'connect.urls'

    # APPS
    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + (
            'django.contrib.sites',
            'django.contrib.flatpages',
            'django.contrib.humanize',
            'django_behave',
            'django_gravatar',
            'endless_pagination',
            'parsley',
            'connect',
            'connect.config',
            'connect.accounts',
            'connect.moderation',
            'connect.discover',
            'bdd',
        )

    # MIDDLEWARE
    @property
    def MIDDLEWARE_CLASSES(self):
        return super().MIDDLEWARE_CLASSES + (
            'django.contrib.sites.middleware.CurrentSiteMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
        )

    # SECURITY
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
    SECRET_KEY = os.getenv('SECRET_KEY',
                           'jj4ie+#b4h=ovjrma7ad*0vhuu8j4fi@8beksc-f+pa_co')

    # Allow all host headers
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # TESTING
    TEST_RUNNER = 'django_behave.runner.DjangoBehaveTestSuiteRunner'

    # DATABASE
    # override this config by setting an environment called DATABASE_URL,
    # eg: postgres://username:password@ip-addres:port/database-name
    # or: sqlite:///path/to/my-database.sqlite3
    DATABASES = {
        'default': dj_database_url.config(
            default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite')
        )
    }

    # TIME / LOCATION CONFIGURATION
    TIME_ZONE = 'Australia/Melbourne'
    LANGUAGE_CODE = 'en'
    LANGUAGES = (
        ('en', _('English')),
    )
    LOCALE_PATHS = (
        os.path.join(BASE_DIR, 'locale'),
    )

    # MEDIA
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

    # AUTH
    AUTH_USER_MODEL = 'accounts.CustomUser'
    LOGIN_REDIRECT_URL = '/'

    # EMAIL
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

    # CACHING
    # Do this here because thanks to django-pylibmc-sasl and pylibmc
    # memcacheify (used on heroku) is painful to install on windows.
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': ''
        }
    }

    # LOGGING
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

    # --- BEGIN CONFIGURATIONS FOR THIRD-PARTY APPS --- #

    # ENDLESS PAGINATION
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
    )

    ENDLESS_PAGINATION_PREVIOUS_LABEL = '<i class="fa fa-chevron-left"></i>'
    ENDLESS_PAGINATION_NEXT_LABEL = '<i class="fa fa-chevron-right"></i>'

    # GRAVATAR
    # See: https://github.com/twaddington/django-gravatar/#configuring
    GRAVATAR_DEFAULT_IMAGE = 'retro'


class LocalSettings(BaseSettings):
    # DEBUG
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = True

    # APPS / DEBUG TOOLBAR
    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + (
            'debug_toolbar',
            'django_extensions',
        )

    @property
    def MIDDLEWARE_CLASSES(self):
        return super().MIDDLEWARE_CLASSES + (
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        )

    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'SHOW_TEMPLATE_CONTEXT': True,
    }


class StagingSettings(BaseSettings):
    # EMAIL
    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ('djrill',)

    EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'
    MANDRILL_API_KEY = os.getenv('MANDRILL_API_KEY')

    # WSGI
    WSGI_APPLICATION = 'connect.wsgi.application'

    # STATIC
    STATIC_ROOT = os.path.join(BASE_DIR, 'connect/static/')

    # DATABASE
    # set this config by setting an environment called DATABASE_URL,
    # eg: postgres://username:password@ip-addres:port/database-name
    DATABASES = {
        'default': dj_database_url.config(
            default='postgres://connectuser:password@localhost:5432/connectdb'
        )
    }


class ProductionSettings(StagingSettings):
    pass


# Now, let's activate our settings
MODE = os.getenv('DJANGO_MODE', 'Local')
cbs.apply('{}Settings'.format(MODE.title()), globals())
