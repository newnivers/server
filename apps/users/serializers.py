from rest_framework.fields import ListField
from rest_framework.serializers import ModelSerializer

from apps.users.models import User


class UserSerializer(ModelSerializer):
    purchase_list = ListField(read_only=True, default=[])
    review_list = ListField(read_only=True, default=[])

    class Meta:
        model = User
        fields = (
            "id",
            "nickname",
            "purchase_list",
            "review_list",
        )
