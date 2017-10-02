"""
Django settings for Asteria project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/

For considerations when deploying to production, see
https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/
"""

from datetime                import datetime  as dt
from django.contrib.messages import constants as messages
from django.utils            import timezone
from configparser            import ConfigParser
from os                      import path      as os_path, environ
from uuid                    import uuid4

# Build paths inside the project like this: os_path.join(BASE_DIR, ...)
BASE_DIR = os_path.dirname(os_path.dirname(os_path.abspath(__file__)))

config = ConfigParser()
config.read(os_path.join(BASE_DIR, 'asteria.config'))

SECRET_KEY = config['Application']['Secret key']
if not SECRET_KEY:
    SECRET_KEY = str(uuid4())

ADMINS = list()
for name, email in config['Admins'].items():
    ADMINS.append((name, email))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config['Application'].getboolean('Debug mode')

TITLE = config['Application']['Title']

ALLOWED_HOSTS = [host.strip() for host in config['Application']['Allowed hosts'].split(',')]

SECURE_CONTENT_TYPE_NOSNIFF = config['Application'].getboolean('Use TLS')
SECURE_BROWSER_XSS_FILTER   = config['Application'].getboolean('Use TLS')
SECURE_SSL_REDIRECT         = config['Application'].getboolean('Use TLS')
SESSION_COOKIE_SECURE       = config['Application'].getboolean('Use TLS')
CSRF_COOKIE_SECURE          = config['Application'].getboolean('Use TLS')
X_FRAME_OPTIONS             = 'DENY'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = config['Application']['Language code']

TIME_ZONE = config['Application']['Time zone']
USE_TZ    = True
USE_I18N  = True
USE_L10N  = True

DT_FMT             = '%Y-%m-%d %H:%M:%S'
REGISTRATION_START = dt.strptime(config['Events']['Registration start'], DT_FMT)
CTF_START          = dt.strptime(config['Events']['CTF start'         ], DT_FMT)
REGISTRATION_END   = dt.strptime(config['Events']['Registration end'  ], DT_FMT)
CTF_END            = dt.strptime(config['Events']['CTF end'           ], DT_FMT)
REGISTRATION_START = timezone.make_aware(REGISTRATION_START)
CTF_START          = timezone.make_aware(CTF_START         )
REGISTRATION_END   = timezone.make_aware(REGISTRATION_END  )
CTF_END            = timezone.make_aware(CTF_END           )

MAX_TEAM_SIZE = int(config['Teams']['Max team size'])

LOGIN_URL           = 'login'
LOGIN_REDIRECT_URL  = 'challenges'
LOGOUT_REDIRECT_URL = 'announcements'

# Application definition
INSTALLED_APPS = [
    # Asteria apps
    'announcements',
    'challenges',
    'teams',
    'tests',
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os_path.join(config['Directories']['Root'], 'common')],
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

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE'  : config['Database']['Backend' ],
        'HOST'    : config['Database']['Host'    ],
        'PORT'    : config['Database']['Port'    ],
        'NAME'    : config['Database']['Name'    ],
        'USER'    : config['Database']['User'    ],
        'PASSWORD': config['Database']['Password'],
        'TEST': {
            'NAME': os_path.join(BASE_DIR, 'test_db.sqlite3'),
        },
    }
}

if 'sqlite3' not in DATABASES['default']['ENGINE']:
    DATABASES['default']['OPTIONS'] = {
        'sql_mode': 'STRICT_ALL_TABLES',
    }

EMAIL_BACKEND       = config['Email']['Backend'        ]
EMAIL_HOST          = config['Email']['Host'           ]
EMAIL_PORT          = config['Email']['Port'           ]
EMAIL_HOST_USER     = config['Email']['User'           ]
EMAIL_HOST_PASSWORD = config['Email']['Password'       ]
DEFAULT_FROM_EMAIL  = config['Email']['Default address']
SERVER_EMAIL        = config['Email']['Server address' ]
EMAIL_USE_TLS       = config['Email'].getboolean('Use TLS')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_ROOT = config['Directories']['Static']
STATIC_URL  = '/static/'
MEDIA_ROOT  = config['Directories']['Media']
MEDIA_URL   = '/media/'

STATICFILES_DIRS = [
    os_path.join(config['Directories']['Root'], 'common/static'),
]

ROOT_URLCONF    = 'asteria.urls'
AUTH_USER_MODEL = 'teams.Player'
MESSAGE_TAGS    = {messages.ERROR: 'danger'}

CACHES = {
    'default': {
        'TIMEOUT': 30,
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

