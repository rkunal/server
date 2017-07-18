from base import *

SECRET_KEY = 'au0ycktkzvp(uxmna*q7nz*wt22-30j(wmw0c&i_mwqe(b^3i_'

DEBUG = False

ALLOWED_HOSTS = ['http://nyaaya.in',]

INSTALLED_APPS += (
    'django.contrib.sites',
)

SITE_ID = 1

import dj_database_url
db_config = dj_database_url.config(default='postgres://nyaaya_web:password@localhost:5432/website')
db_config['ATOMIC_REQUESTS'] = False
DATABASES = {
    'default': db_config,
}

DEFAULT_FILE_STORAGE = "server.s3utils.MediaRootS3Boto3Storage"

AWS_STORAGE_BUCKET_NAME = 'BUCKETNAME'
AWS_S3_REGION_NAME = 'ap-south-1'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = True
AWS_ACCESS_KEY_ID = 'XXXXXXX'
AWS_SECRET_ACCESS_KEY = 'XXXXXXXX'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, "assets")


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
