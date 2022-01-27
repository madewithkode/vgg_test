from vgg_interview.settings.base import *
import os

from dotenv import load_dotenv

load_dotenv()

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DATABASE_HOST'),
        'USER': os.environ.get('DATABASE_USERNAME'),
        'NAME': os.environ.get('DATABASE_NAME'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'PORT': 5432,
    },
}

ALLOWED_HOSTS=['*']

DEBUG = bool(int(os.environ.get('DEBUG', 0)))


########## CELERY CONFIGS ##############
BROKER_URL = os.environ.get('BROKER_URL')
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
BROKER_BACKEND = 'memory'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600, 'fanout_prefix': True, 'fanout_patterns': True}  # 1 hour

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



