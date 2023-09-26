from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.itercompat import is_iterable
from django.utils.translation import gettext_lazy as _

from apps.users.managers import UserManager


class User(AbstractBaseUser):
    nickname = models.CharField(
        verbose_name=_("nickname"),
        max_length=31,
        validators=[UnicodeUsernameValidator()],
    )
    social_id = models.CharField(verbose_name=_("social id"), max_length=31)
    is_admin = models.BooleanField(verbose_name=_("admin status"), default=False)
    is_superuser = models.BooleanField(
        verbose_name=_("superuser status"), default=False
    )

    objects = UserManager()

    USERNAME_FIELD = "nickname"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-id"]

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_superuser

    def has_perms(self, perm_list, obj=None):
        if not is_iterable(perm_list) or isinstance(perm_list, str):
            raise ValueError(_("perm_list must be an iterable of permissions."))

        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        return self.is_active and self.is_superuser
