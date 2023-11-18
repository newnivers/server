from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampModel


class Place(TimeStampModel):
    name = models.CharField(max_length=31, verbose_name=_("name"))

    class Meta:
        verbose_name = _("place")
        verbose_name_plural = _("places")
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Seat(models.Model):
    place = models.ForeignKey(
        "places.Place",
        on_delete=models.CASCADE,
        related_name="seats",
        verbose_name=_("place"),
    )
    column = models.CharField(max_length=3, verbose_name=_("column"))
    row = models.CharField(max_length=7, verbose_name=_("row"))

    class Meta:
        verbose_name = _("seat")
        verbose_name_plural = _("seats")
        ordering = ["-id"]

    def __str__(self):
        return f"{self.column}{self.row}"
