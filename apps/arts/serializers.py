from rest_framework.serializers import ModelSerializer

from apps.arts.models import Art


class ArtSerializer(ModelSerializer):
    class Meta:
        model = Art
        fields = []
