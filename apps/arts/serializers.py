from rest_framework.serializers import ModelSerializer

from apps.arts.models import Art
from apps.places.serializers import PlaceSerializer


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
            "purchase_limit_count",
        ]
