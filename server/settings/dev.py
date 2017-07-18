from base import *

DEBUG = True

INSTALLED_APPS += (
    'corsheaders',
)

MIDDLEWARE += [
    'corsheaders.middleware.CorsMiddleware',
]

import dj_database_url
db_config = dj_database_url.config(default='postgres://nyaaya_web:password@localhost:5432/website')
db_config['ATOMIC_REQUESTS'] = False
DATABASES = {
    'default': db_config,
}

CORS_ORIGIN_ALLOW_ALL = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console','file'],
            'level': 'DEBUG'
        },
        'django.db.backends': {
            'handlers': None,  # Quiet by default!
            'propagate': False,
            'level':'DEBUG',
        },
        'django': {
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'django.template': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
