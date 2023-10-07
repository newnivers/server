from django.db import models
from django.utils.translation import gettext_lazy as _


class CategoryChoices(models.TextChoices):
    EXHIBITION = "EXHI", _("전시")
    SHOW = "SHOW", _("공연")


class GenreChoices(models.TextChoices):
    THEATER = "THEA", _("연극")
    MUSICAL = "MUSI", _("뮤지컬")
    CONCERT = "CONC", _("콘서트")
    DANCE = "DANC", _("무용")
    CHILDREN = "CHIL", _("아동")
    PREVIEW = "PREV", _("시사회")
    EXHIBITION = "EXHI", _("전시")
    FESTIVAL = "FEST", _("축제")
    LECTURE = "LECT", _("강의")


class StatusChoices(models.TextChoices):
    PENDING = "PEND", _("검수중")
    REJECTED = "REJECTED", _("거부")
    APPROVED = "APPROVED", _("허용")
