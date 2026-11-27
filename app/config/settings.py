import os

SECRET_KEY = os.environ.get('CAT_SECRET', 'local-development-secret')
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
ROOT_URLCONF = 'config.urls'
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'accounts',
    'coredata',
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
        'CONN_MAX_AGE': 0,
    }
}
