# Generated by Django 4.2.5 on 2023-10-16 12:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("arts", "0003_art_place_artschedule_art_ticket_art"),
    ]

    operations = [
        migrations.AlterField(
            model_name="art",
            name="image",
            field=models.URLField(verbose_name="image"),
        ),
    ]
