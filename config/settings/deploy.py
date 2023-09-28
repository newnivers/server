import os

from config.settings import *  # noqa

DEBUG = False
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

INSTALLED_APPS += [
    "corsheaders",
]

MIDDLEWARE += [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGIN_REGEXES = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]
