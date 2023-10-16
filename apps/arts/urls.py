from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.arts.views import ArtViewSet

app_name = "arts"

router = DefaultRouter(trailing_slash=False)
router.register("", ArtViewSet, "arts")


urlpatterns = [
    path("", include(router.urls)),
]
