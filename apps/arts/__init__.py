from django.db import models
from django.utils.translation import gettext_lazy as _


class CategoryChoices(models.TextChoices):
    EXHIBITION = "EXHIBITION", _("전시")
    SHOW = "SHOW", _("공연")


class StatusChoices(models.TextChoices):
    PENDING = "PENDING", _("검수중")
    REJECTED = "REJECTED", _("거부")
    APPROVED = "APPROVED", _("허용")
