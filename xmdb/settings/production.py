from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'xmdb.herokuapp.com'
]

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'