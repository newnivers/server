from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.places.views import PlaceViewSet

app_name = "places"

router = DefaultRouter(trailing_slash=False)
router.register("", PlaceViewSet, "places")


urlpatterns = [
    path("", include(router.urls)),
]
