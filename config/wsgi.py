from django.core.wsgi import get_wsgi_application

from config.utils import set_environment

set_environment()
application = get_wsgi_application()
