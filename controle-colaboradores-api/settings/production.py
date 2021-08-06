from .base import *

DEBUG = False

ADMINS = [('Hélder', 'helderlgoliveira@gmail.com')]
ALLOWED_HOSTS = ['']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

## Original - Padrão:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

"""
# Email produção

EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = 'no-reply@fusion.com.br'
EMAIL_PORT = 587
EMAIL_USE_TSL = True
EMAIL_HOST_PASSWORD = 'fusion'
DEFAULT_FROM_EMAIL = 'contato@fusion.com.br'
"""

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
