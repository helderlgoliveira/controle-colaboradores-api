from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['*']

# ADMINS: A list of all the people who get code error notifications.
# When DEBUG=False and AdminEmailHandler is configured in LOGGING (done by default),
# Django emails these people the details of exceptions raised in the request/response cycle.
ADMINS = [('Hélder', 'helderlgoliveira@gmail.com')]

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