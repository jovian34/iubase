# Generated by Django 5.0 on 2024-01-01 23:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("live_game_blog", "0012_blogentry_is_raw_html"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogentry",
            name="is_raw_html",
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
