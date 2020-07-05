"""
Django settings for Asteria project.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/

For considerations when deploying to production, see
https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
"""

from configparser import (
    ConfigParser
)
from datetime import (
    datetime as dt
)
from pathlib import (
    Path
)
from uuid import (
    uuid4
)
from django.contrib.messages import (
    constants as messages
)
from django.utils import (
    timezone
)


BASE_DIR = Path(__file__).resolve().parent.parent

config = ConfigParser()
config.read(BASE_DIR.joinpath('asteria.config'))

application_config = config['Application']

SECRET_KEY = application_config['Secret key']
if not SECRET_KEY:
    SECRET_KEY = str(uuid4())

ADMINS = list()
for name, email in config['Admins'].items():
    ADMINS.append((name, email))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('Application', 'Debug mode')

TITLE = application_config['Title']

ALLOWED_HOSTS = [host.strip() for host in application_config['Allowed hosts'].split(',')]

use_tls = config.getboolean('Application', 'Use TLS')
SECURE_CONTENT_TYPE_NOSNIFF = use_tls
SECURE_BROWSER_XSS_FILTER   = use_tls
SECURE_SSL_REDIRECT         = use_tls
SESSION_COOKIE_SECURE       = use_tls
CSRF_COOKIE_SECURE          = use_tls
X_FRAME_OPTIONS = 'DENY'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = application_config['Language code']

TIME_ZONE = application_config['Time zone']
USE_TZ   = True
USE_I18N = True
USE_L10N = True

DT_FMT = '%Y-%m-%d %H:%M:%S'
events_config = config['Events']
REGISTRATION_START = dt.strptime(events_config['Registration start'], DT_FMT)
CTF_START          = dt.strptime(events_config['CTF start'         ], DT_FMT)
REGISTRATION_END   = dt.strptime(events_config['Registration end'  ], DT_FMT)
CTF_END            = dt.strptime(events_config['CTF end'           ], DT_FMT)

REGISTRATION_START = timezone.make_aware(REGISTRATION_START)
CTF_START          = timezone.make_aware(CTF_START         )
REGISTRATION_END   = timezone.make_aware(REGISTRATION_END  )
CTF_END            = timezone.make_aware(CTF_END           )

MAX_TEAM_SIZE = config.getint('Teams', 'Max team size')

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

dir_config = config['Directories']
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path(dir_config['Root']).joinpath('common')],
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
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
db_config = config['Database']
DATABASES = {
    'default': {
        'ENGINE'  : db_config['Backend' ],
        'HOST'    : db_config['Host'    ],
        'PORT'    : db_config['Port'    ],
        'NAME'    : db_config['Name'    ],
        'USER'    : db_config['User'    ],
        'PASSWORD': db_config['Password'],
        'TEST': {
            'NAME': BASE_DIR.joinpath('test_db.sqlite3'),
        },
    }
}

if 'sqlite3' not in DATABASES['default']['ENGINE']:
    DATABASES['default']['OPTIONS'] = {
        'sql_mode': 'STRICT_ALL_TABLES',
    }

email_config = config['Email']
EMAIL_BACKEND       = email_config['Backend'        ]
EMAIL_HOST          = email_config['Host'           ]
EMAIL_PORT          = email_config['Port'           ]
EMAIL_HOST_USER     = email_config['User'           ]
EMAIL_HOST_PASSWORD = email_config['Password'       ]
DEFAULT_FROM_EMAIL  = email_config['Default address']
SERVER_EMAIL        = email_config['Server address' ]
EMAIL_USE_TLS       = email_config.getboolean('Use TLS')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = dir_config['Static']
STATIC_URL  = '/static/'
MEDIA_ROOT  = dir_config['Media']
MEDIA_URL   = '/media/'

STATICFILES_DIRS = [
    Path(dir_config['Root']).joinpath('common/static'),
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

