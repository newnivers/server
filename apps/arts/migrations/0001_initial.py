# Generated by Django 4.2.5 on 2023-11-18 08:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("places", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Art",
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
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated_at"),
                ),
                ("title", models.CharField(max_length=31, verbose_name="title")),
                ("image", models.URLField(verbose_name="image")),
                ("genre", models.CharField(max_length=15, verbose_name="genre")),
                (
                    "category",
                    models.CharField(
                        choices=[("EXHIBITION", "전시"), ("SHOW", "공연")],
                        max_length=15,
                        verbose_name="category",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "검수중"),
                            ("REJECTED", "거부"),
                            ("APPROVED", "허용"),
                        ],
                        default="PENDING",
                        max_length=15,
                        verbose_name="status",
                    ),
                ),
                (
                    "running_time",
                    models.PositiveIntegerField(verbose_name="running time"),
                ),
                (
                    "age_limit",
                    models.PositiveIntegerField(default=0, verbose_name="age limit"),
                ),
                (
                    "inter_mission",
                    models.PositiveIntegerField(
                        default=0, verbose_name="inter mission"
                    ),
                ),
                ("description", models.TextField(verbose_name="description")),
                (
                    "caution_description",
                    models.TextField(verbose_name="caution description"),
                ),
                (
                    "cs_phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None
                    ),
                ),
                ("reserved_seat", models.BooleanField(default=False)),
                ("is_free", models.BooleanField(default=False)),
                (
                    "purchase_limit_count",
                    models.PositiveIntegerField(
                        default=1, verbose_name="limit purchase count"
                    ),
                ),
                (
                    "price_currency",
                    djmoney.models.fields.CurrencyField(
                        choices=[("KRW", "South Korean Won")],
                        default="KRW",
                        editable=False,
                        max_length=3,
                    ),
                ),
                (
                    "price",
                    djmoney.models.fields.MoneyField(
                        decimal_places=2,
                        default_currency="KRW",
                        max_digits=15,
                        verbose_name="price",
                    ),
                ),
                (
                    "place",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="arts",
                        to="places.place",
                        verbose_name="place",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="arts",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="create by",
                    ),
                ),
            ],
            options={
                "verbose_name": "art",
                "verbose_name_plural": "arts",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="ArtSchedule",
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
                ("start_at", models.DateTimeField(verbose_name="start at")),
                ("end_at", models.DateTimeField(verbose_name="end at")),
                ("seat_count", models.PositiveIntegerField(verbose_name="seat count")),
                (
                    "art",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedules",
                        to="arts.art",
                        verbose_name="art schedule",
                    ),
                ),
            ],
            options={
                "verbose_name": "art schedule",
                "verbose_name_plural": "art schedules",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Ticket",
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
                (
                    "art_schedule",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tickets",
                        to="arts.artschedule",
                        verbose_name="create by",
                    ),
                ),
                (
                    "seat",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tickets",
                        to="places.seat",
                        verbose_name="seat",
                    ),
                ),
            ],
            options={
                "verbose_name": "ticket",
                "verbose_name_plural": "tickets",
                "ordering": ["-id"],
            },
        ),
        migrations.AddConstraint(
            model_name="artschedule",
            constraint=models.UniqueConstraint(
                fields=("art", "start_at"), name="unique schedule start at"
            ),
        ),
        migrations.AddConstraint(
            model_name="artschedule",
            constraint=models.UniqueConstraint(
                fields=("art", "end_at"), name="unique schedule end at"
            ),
        ),
    ]
