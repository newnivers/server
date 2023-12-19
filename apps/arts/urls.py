from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.arts.views import ArtViewSet, TicketViewSet

app_name = "arts"

router = DefaultRouter(trailing_slash=False)
router.register("", ArtViewSet, "arts")
ticket_router = DefaultRouter(trailing_slash=False)
ticket_router.register("", TicketViewSet, "tickets")


urlpatterns = [
    path("", include(router.urls)),
    path("tickets/", include(ticket_router.urls)),
]
