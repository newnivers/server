from django.db import IntegrityError
from django.db.transaction import atomic
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.arts.models import Art, ArtSchedule


class ArtScheduleSerializer(ModelSerializer):
    class Meta:
        model = ArtSchedule
        fields = [
            "id",
            "start_at",
            "end_at",
            "seat_count",
        ]

    def validate(self, data):
        start_at = data.get("start_at")
        end_at = data.get("end_at")

        if start_at and end_at and start_at > end_at:
            raise serializers.ValidationError(
                {"start_at": "start_at은 end_at보다 클 수 없습니다."}
            )

        return super().validate(data)


class ArtSerializer(ModelSerializer):
    schedules = ArtScheduleSerializer(many=True)

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
            "age_limit",
            "inter_mission",
            "description",
            "caution_description",
            "cs_phone_number",
            "reserved_seat",
            "start_date",
            "end_date",
            "is_free",
            "purchase_limit_count",
            "price",
            "schedules",
            "ticket_open_at",
            "ticket_close_at",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        is_free = data.get("is_free", None)
        price = data.get("price", None)
        ticket_open_at = data.get("ticket_open_at", None)
        ticket_close_at = data.get("ticket_close_at", None)

        if ticket_open_at and ticket_close_at and ticket_open_at > ticket_close_at:
            raise serializers.ValidationError(
                {"ticket_open_at": "ticket_open_at은 ticket_close_at보다 클 수 없습니다."}
            )

        if is_free and price > 0:
            raise serializers.ValidationError(
                {"is_free": "is_free가 true일때 price는 0이여야만 합니다."}
            )

        return super().validate(data)

    @atomic
    def create(self, validated_data):
        schedules_data = validated_data.pop("schedules", [])
        validated_data["user"] = self.context.get("request").user
        art_instance = super().create(validated_data)
        art_schedules = [
            ArtSchedule(art=art_instance, **schedule_data)
            for schedule_data in schedules_data
        ]
        try:
            ArtSchedule.objects.bulk_create(art_schedules)
        except IntegrityError:
            raise serializers.ValidationError(
                {"schedules": "중복된 start_at 또는 end_at 값은 입력할 수 없습니다."},
            )
        return art_instance

    @atomic
    def update(self, instance, validated_data):
        schedules_data = validated_data.pop("schedules", [])
        validated_data["user"] = self.context.get("request").user
        art_instance = super().update(instance, validated_data)
        art_schedules = [
            ArtSchedule(art=art_instance, **schedule_data)
            for schedule_data in schedules_data
        ]
        try:
            art_instance.schedules.all().delete()
            ArtSchedule.objects.bulk_create(art_schedules)
        except IntegrityError:
            raise serializers.ValidationError(
                {"schedules": "중복된 start_at 또는 end_at 값은 입력할 수 없습니다."},
            )
        return art_instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        place = representation.get("place", None)
        if place:
            representation["place"] = instance.place.name
        representation["schedules"] = ArtScheduleSerializer(
            instance.schedules.all(), many=True
        ).data
        return representation
