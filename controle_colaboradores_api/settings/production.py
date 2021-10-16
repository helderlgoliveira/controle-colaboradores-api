from .base import *

DEBUG = False

# TODO Definir os admins e os allowed_hosts:
ADMINS = [('Hélder', 'helderlgoliveira@gmail.com')]
ALLOWED_HOSTS = ['']

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

# TODO Definir as configurações de e-mail:
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = 587
EMAIL_USE_TSL = True
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = ''

# Recursos Extras de Segurança do Django
SECURE_HSTS_SECONDS = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True
