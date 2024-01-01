from django.urls import include, path

urlpatterns = [
    path("users/", include("apps.users.urls")),
    path("", include("apps.arts.urls")),
    path("places/", include("apps.places.urls")),
]
