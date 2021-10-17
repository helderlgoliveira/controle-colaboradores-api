import dj_database_url

from .production import *

DATABASES = {
    'default': dj_database_url.config()
}