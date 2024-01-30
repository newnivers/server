from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from apps.arts.views import ArtViewSet, TicketViewSet, CommentViewSet, ArtScheduleViewSet

app_name = "arts"

router = DefaultRouter(trailing_slash=False)
router.register("arts", ArtViewSet, "arts")
ticket_router = DefaultRouter(trailing_slash=False)
ticket_router.register("", TicketViewSet, "tickets")

comment_router = NestedDefaultRouter(router, r'arts', lookup='art')
comment_router.register(r'comments', CommentViewSet)

art_schedule_router = DefaultRouter(trailing_slash=False)
art_schedule_router.register(r"art_schedules", ArtScheduleViewSet, "art_schedules")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(comment_router.urls)),
    path("", include(art_schedule_router.urls)),
    path("arts/tickets/", include(ticket_router.urls)),
]
