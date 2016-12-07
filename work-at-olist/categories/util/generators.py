from django.conf import settings

import tokenlib


def generate_uid(**kwargs):
    return tokenlib.make_token(kwargs, secret=settings.SECRET_KEY)
