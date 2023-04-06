from .common import *

DEBUG = False

# Delete unused in production applications
INSTALLED_APPS.remove('drf_yasg')

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

BASE_URL = os.environ.get('BASE_URL')
BASE_CLIENT_URL = os.environ.get('BASE_CLIENT_URL')

# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

STATIC_URL = '/static/'
MEDIA_PATH = 'media'
MEDIA_URL = '%s/%s/' % (BASE_URL, MEDIA_PATH)
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

ADMINS = [('Vladimir', 'titanitewow@gmail.com')]

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
        'django': {
            'handlers': ['console', 'console_errors', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'console_errors'],
            'propagate': False,
            'level': 'DEBUG'
        },
    },
}
