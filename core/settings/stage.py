from .common import *

DEBUG = False

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'stage)(r$zokmzkv)6=jrde6vu)94as0(^&-l%4mya4inm%#b1^_gf+')

LOG_PATH = os.path.join(BASE_DIR, '../logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout
        },
        'console_errors': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stderr
        },
    },
    'root': {
        'handlers': ['console_errors'],
        'level': 'WARNING',
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'console_errors'],
            'propagate': False,
            'level': 'DEBUG'
        },
    },
}