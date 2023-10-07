from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.arts import CategoryChoices, GenreChoices, StatusChoices
from apps.core.models import TimeStampModel


class Art(TimeStampModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="arts",
        null=True,
        verbose_name=_("create by"),
    )
    title = models.CharField(
        verbose_name=_("title"),
        max_length=31,
    )
    image = models.ImageField(
        upload_to="arts",
        verbose_name=_("image"),
    )
    genre = models.CharField(
        max_length=7,
        choices=GenreChoices.choices,
        verbose_name=_("genre"),
    )
    category = models.CharField(
        max_length=7,
        choices=CategoryChoices.choices,
        verbose_name=_("category"),
    )
    status = models.CharField(
        max_length=15,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name=_("status"),
    )
    running_time = models.PositiveIntegerField(
        default=0,
        verbose_name=_("running time"),
    )
    age_limit = models.PositiveIntegerField(
        default=0,
        verbose_name=_("age limit"),
    )
    inter_mission = models.PositiveIntegerField(
        default=0,
        verbose_name=_("inter mission"),
    )
    description = models.TextField(
        verbose_name=_("description"),
    )
    caution_description = models.TextField(
        verbose_name=_("caution description"),
    )
    cs_phone_number = PhoneNumberField()
    start_date = models.DateField(
        verbose_name=_("start date"),
    )
    end_date = models.DateField(
        verbose_name=_("end date"),
    )


class ArtSchedule(models.Model):
    start_time = models.TimeField(
        verbose_name=_("start time"),
    )
    end_time = models.TimeField(
        verbose_name=_("end time"),
    )
