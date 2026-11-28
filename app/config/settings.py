import os

from django.core.exceptions import ImproperlyConfigured

SECRET_KEY = os.environ.get('CAT_SECRET', 'local-development-secret')
CAT_PROFILE = os.environ.get('CAT_PROFILE', 'demo')
CAT_GATEWAY_SCALE = os.environ.get('CAT_GATEWAY_SCALE', '1')
CAT_PARTNER_KEY = os.environ.get('CAT_PARTNER_KEY', 'local-passgate-26')
CAT_WORKER_ID = os.environ.get('CAT_WORKER_ID', 'worker-1')
if CAT_PROFILE == 'demo' and CAT_GATEWAY_SCALE != '1':
    raise ImproperlyConfigured('CAT_PROFILE=demo requires CAT_GATEWAY_SCALE=1.')
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
ROOT_URLCONF = 'config.urls'
MANAGEMENT_PROVIDER = 'catalog.management.basic_management_snapshot'
MANAGEMENT_PARTIAL = None
MANAGEMENT_OPERATIONS_URLCONF = None
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'accounts',
    'coredata',
    'catraca_platform',
]
MIDDLEWARE = []
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'
USE_TZ = True
TEST_RUNNER = 'config.test_runner.NonEmptyRunner'
TIME_ZONE = 'UTC'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'catraca',
        'HOST': os.environ.get('CAT_DB_HOST', 'db'),
        'USER': os.environ.get('CAT_DB_USER', 'catraca_runtime'),
        'PASSWORD': os.environ.get('CAT_DB_PASSWORD', ''),
        'PORT': os.environ.get('CAT_DB_PORT', '5432'),
        'CONN_MAX_AGE': 0,
    }
}
