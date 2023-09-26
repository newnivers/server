import os
from pathlib import Path

import environ

env = environ.Env(DEBUG=(bool, True), overwrite=True)
environ.Env.read_env(
    env_file=os.path.join(Path(__file__).resolve().parent.parent, ".env")
)


def set_environment():
    match env("ENVIRONMENT"):
        case "DEPLOY":
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.deploy")
        case "DEVELOP":
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.develop")
        case _:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
