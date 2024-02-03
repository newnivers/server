from rest_framework.fields import CharField, ListField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from apps.arts.models import Art, Ticket, Comment
from apps.users.models import User


class PurchaseSerializer(ModelSerializer):
    visitor_count = SerializerMethodField(read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "nickname",
            "art_title",
            "art_thumbnail",
            "place",
            "visitor_count"
        )

    def get_visitor_count(self, obj):
        return Ticket.objects.filter(user=self.context.get("request").user,
                                     art_schedule=obj.art_schedule).count()


class ReviewSerializer(ModelSerializer):
    visitor_count = SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "nickname",
            "art_title",
            "art_thumbnail",
            "place",
            "visitor_count",
        )

    def get_visitor_count(self, obj):
        return Ticket.objects.filter(user=self.context.get("request").user,
                                     art_schedule__art=obj.art).count()


class UserSerializer(ModelSerializer):
    nickname = CharField(required=False)
    purchase_list = SerializerMethodField(read_only=True)
    review_list = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "nickname",
            "profile_image",
            "purchase_list",
            "review_list",
        )

    def get_purchase_list(self, obj):
        targets = []
        target_schedules = []
        for ticket in obj.tickets.all():
            if ticket.art_schedule not in target_schedules:
                target_schedules.append(ticket.art_schedule)
                targets.append(ticket)
            else:
                target_schedules.append(ticket.art_schedule)
        return PurchaseSerializer(targets, many=True, context={'request': self.context.get("request")}).data

    def get_review_list(self, obj):
        return ReviewSerializer(obj.comments.all(), many=True, context={'request': self.context.get("request")}).data
