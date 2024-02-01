from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField

from apps.arts import CategoryChoices, StatusChoices
from apps.core.models import TimeStampModel


class Art(TimeStampModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="arts",
        null=True,
        verbose_name=_("create by"),
    )
    place = models.ForeignKey(
        "places.Place",
        on_delete=models.SET_NULL,
        null=True,
        related_name="arts",
        verbose_name=_("place"),
    )
    title = models.CharField(max_length=31, verbose_name=_("title"))
    image = models.URLField(verbose_name=_("image"))
    genre = models.CharField(max_length=15, verbose_name=_("genre"))
    category = models.CharField(max_length=15, choices=CategoryChoices.choices, verbose_name=_("category"))
    status = models.CharField(
        max_length=15,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name=_("status"),
    )
    running_time = models.PositiveIntegerField(verbose_name=_("running time"))
    age_limit = models.PositiveIntegerField(default=0, verbose_name=_("age limit"))
    inter_mission = models.PositiveIntegerField(default=0, verbose_name=_("inter mission"))
    description = models.TextField(verbose_name=_("description"))
    caution_description = models.TextField(verbose_name=_("caution description"))
    cs_phone_number = PhoneNumberField(null=True, blank=True)
    reserved_seat = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    purchase_limit_count = models.PositiveIntegerField(
        default=1,
        verbose_name=_("limit purchase count"),
    )
    price = MoneyField(
        max_digits=15,
        decimal_places=2,
        default_currency="KRW",
        verbose_name=_("price"),
    )
    ticket_open_at = models.DateTimeField()
    ticket_close_at = models.DateTimeField()
    seat_max_count = models.PositiveIntegerField(default=0)
    hit_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("art")
        verbose_name_plural = _("arts")
        ordering = ["-id"]

    def __str__(self):
        return self.title

    @property
    def created_by(self):
        return self.user.nickname

    @property
    def start_date(self):
        return min(self.schedules.values_list("start_at", flat=True))
    @property
    def end_date(self):
        return max(self.schedules.values_list("end_at", flat=True))


class ArtSchedule(models.Model):
    art = models.ForeignKey(
        "arts.Art",
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name=_("art schedule"),
    )
    start_at = models.DateTimeField(verbose_name=_("start at"))
    end_at = models.DateTimeField(verbose_name=_("end at"))

    class Meta:
        verbose_name = _("art schedule")
        verbose_name_plural = _("art schedules")
        ordering = ["-id"]

        constraints = [
            models.UniqueConstraint(
                fields=["art", "start_at"],
                name="unique schedule start at",
            ),
            models.UniqueConstraint(
                fields=["art", "end_at"],
                name="unique schedule end at",
            ),
        ]

    @property
    def left_seat_count(self):
        return self.tickets.filter(is_sold_out=False).count()

    @property
    def seat_max_count(self):
        return self.art.seat_max_count


class Ticket(models.Model):
    art_schedule = models.ForeignKey(
        "arts.ArtSchedule",
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_("art schedule"),
    )
    seat = models.ForeignKey(
        "places.Seat",
        on_delete=models.SET_NULL,
        null=True,
        related_name="tickets",
        verbose_name=_("seat"),
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
        verbose_name=_("user"),
    )
    qr_code = models.ImageField(upload_to="media/qr", default="", blank=True)
    is_sold_out = models.BooleanField(default=False, verbose_name=_("is sold out"))

    class Meta:
        verbose_name = _("ticket")
        verbose_name_plural = _("tickets")
        ordering = ["-id"]

    @property
    def art_title(self):
        return self.art_schedule.art.title

    @property
    def place(self):
        return self.art_schedule.art.place.name

    @property
    def nickname(self):
        return self.user.nickname

    @property
    def art_schedule_date(self):
        return self.art_schedule.start_at

    @property
    def art_thumbnail(self):
        return self.art_schedule.art.image


class Comment(TimeStampModel):
    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("author"),
    )
    art = models.ForeignKey(
        "arts.Art",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("art"),
    )
    description = models.TextField(verbose_name=_("description"))
    score = models.PositiveIntegerField()

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        ordering = ["-id"]