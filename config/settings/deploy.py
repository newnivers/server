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
    "root": {"level": "DEBUG", "handlers": ["file"]},
    "formatters": {
        "verbose": {
            "format": (
                "%(asctime)s %(levelname)s %(name)s %(message)s"
                " [PID:%(process)d:%(threadName)s]"
            )
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs/mysite.log",
            "maxBytes": 10 * 1024 * 1024,  # 10MB
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
