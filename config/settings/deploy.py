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
    "http://3.37.86.43/",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGIN_REGEXES = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://3.37.86.43/",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "file": {
            "level": "INFO",
            "encoding": "utf-8",
            "filters": ["require_debug_false"],
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs/mysite.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins", "file"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "accounts": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    },
}
