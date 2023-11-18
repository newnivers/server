# Generated by Django 4.2.5 on 2023-11-18 04:28

import apps.users.managers
import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "nickname",
                    models.CharField(
                        max_length=31,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="nickname",
                    ),
                ),
                (
                    "social_id",
                    models.CharField(max_length=63, verbose_name="social id"),
                ),
                (
                    "profile_image",
                    models.URLField(
                        blank=True, default="", verbose_name="profile image"
                    ),
                ),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="is deleted"),
                ),
                (
                    "is_admin",
                    models.BooleanField(default=False, verbose_name="admin status"),
                ),
                (
                    "is_superuser",
                    models.BooleanField(default=False, verbose_name="superuser status"),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "ordering": ["-id"],
            },
            managers=[
                ("objects", apps.users.managers.UserManager()),
            ],
        ),
    ]
