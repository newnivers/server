from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.views import DevAuthView, UserViewSet
from config.utils import env

app_name = "users"

router = DefaultRouter(trailing_slash=False)
router.register("", UserViewSet, "users")


urlpatterns = [
    path("", include(router.urls)),
]

if env("ENVIRONMENT") in ("DEVELOP", "LOCAL"):
    dev_router = DefaultRouter(trailing_slash=False)
    dev_router.register("", DevAuthView, "dev")
    urlpatterns += [
        path("", include(dev_router.urls)),
    ]
