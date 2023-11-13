from rest_framework.serializers import ModelSerializer

from apps.places.models import Place


class PlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = [
            "id",
            "name",
        ]
