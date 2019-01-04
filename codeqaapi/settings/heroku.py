""" Heroku setting configuration
"""
# Define here heroku specific settings

from decouple import config
import dj_database_url

from .base import *

DEBUG = False

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}
