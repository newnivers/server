from rest_framework.serializers import ModelSerializer

from apps.arts.models import Art
from apps.places.models import Place


class PlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = [
            "id",
            "name",
        ]


class ArtSerializer(ModelSerializer):
    place = PlaceSerializer(read_only=True)

    class Meta:
        model = Art
        fields = [
            "id",
            "user",
            "place",
            "title",
            "image",
            "genre",
            "category",
            "status",
            "running_time",
            "inter_mission",
            "description",
            "caution_description",
            "cs_phone_number",
            "start_date",
            "end_date",
            "is_free",
            "limit_purchase_count",
        ]