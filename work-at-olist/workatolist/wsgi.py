"""
WSGI config for workatolist project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
from prettyconf import config

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workatolist.settings")

application = get_wsgi_application()

if config('HEROKU', default=False):
    from whitenoise.django import DjangoWhiteNoise
    application = DjangoWhiteNoise(application)
    print('whitenoise')
