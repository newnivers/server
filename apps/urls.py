from django.urls import include, path

urlpatterns = [
    path("users/", include("apps.users.urls")),
    path("arts/", include("apps.arts.urls")),
]
