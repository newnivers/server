from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.views import UserViewSet

app_name = "users"

router = DefaultRouter(trailing_slash=False)
router.register("", UserViewSet, "users")


urlpatterns = [
    path("", include(router.urls)),
]
