# import imp
import importlib
from django.apps import AppConfig


class pgsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pgsApp'
