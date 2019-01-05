"""
Development configurations
"""

# Define development specific settings

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'codeqa',
        'HOST': 'localhost',
        'USER': 'postgres',
        'PASSWORD': '',
        'PORT': '5432'
    }
}
