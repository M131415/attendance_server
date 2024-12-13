import os 
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', '10.0.2.2', ]

"""
CORS_ALLOWED_ORIGINS = [
    "http://localhost:34027",
    "http://127.0.0.1:41271",
    "http://com.example.asistencia_jaguar"
]
"""

CORS_ALLOW_ALL_ORIGINS: True

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')