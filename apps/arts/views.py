from rest_framework import mixins

from apps.arts.models import Art
from apps.arts.serializers import ArtSerializer
from apps.core.views import BaseViewSet


class ArtViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    BaseViewSet,
):
    queryset = Art.objects.all()
    serializer_class = ArtSerializer
