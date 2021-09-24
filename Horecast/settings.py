from pathlib import Path
import dj_database_url
import os
import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = []

# AWS
env = environ.Env()
# env.read_env(os.path.join(BASE_DIR, '.env'))
# SECRET_KEY = env('SECRET_KEY')
# DEBUG = env('DEBUG')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'forecast.apps.ForecastConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'Horecast.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'forecast.context_processors.searchform',
            ],
        },
    },
]

WSGI_APPLICATION = 'Horecast.wsgi.application'

# DATABASES = {
#     'default': env.db(),
# }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = 'forecast/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FOWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'forecast/static')

DEBUG = False

try:
    from .local_settings import *
except ImportError:
    pass

if not DEBUG:
    SECRET_KEY = os.environ['SECRET_KEY']
    # AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    # AWS_SECRET_ACCESS_KEY= os.environ['AWS_SECRET_ACCESS_KEY']
    # AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    # AWS_S3_REGION_NAME = os.environ['AWS_S3_REGION_NAME']
    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
