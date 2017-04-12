"""
WSGI config for automobile project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
import sys
from os.path import join,dirname,abspath

path = '/home/wangxr1108/mysite/automobile/AutomobilePrediction'
#root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)
#if path not in sys.path:
#    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'automobile.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()