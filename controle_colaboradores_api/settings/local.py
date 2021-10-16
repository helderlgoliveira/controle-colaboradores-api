from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DATABASE_NAME"),
        'USER': os.getenv("DATABASE_USER"),
        'PASSWORD': os.getenv("DATABASE_PASSWORD"),
        'HOST': os.getenv("DATABASE_HOST"),
        'PORT': os.getenv("DATABASE_PORT")
    }
}