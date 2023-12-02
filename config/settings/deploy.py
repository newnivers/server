import os

from config.settings import *  # noqa

DEBUG = False

INSTALLED_APPS += [
    "corsheaders",
    "storages",
]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.JsonWebTokenMiddleWare",
]


CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://3.37.86.43",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "DEBUG", "handlers": ["file"]},
    "formatters": {
        "verbose": {"format": ("%(asctime)s %(levelname)s %(name)s %(message)s" " [PID:%(process)d:%(threadName)s]")},
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs/application.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
        }
    },
    "loggers": {
        "django": {"handlers": ["file"], "level": "INFO", "propagate": True},
        "django.server": {"handlers": ["file"], "level": "INFO", "propagate": True},
        "django.db.backends": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
        "unicommerce": {"handlers": ["file"], "level": "INFO", "propagate": True},
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, "static")

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_REGION = "ap-northeast-2"

AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = "%s.s3.%s.amazonaws.com" % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
