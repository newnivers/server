# Generated by Django 4.2.5 on 2024-01-21 07:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("places", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="place",
            name="is_reserved_seat",
            field=models.BooleanField(default=True),
        ),
    ]
