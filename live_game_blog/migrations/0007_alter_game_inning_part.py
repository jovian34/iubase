# Generated by Django 5.0 on 2023-12-27 17:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("live_game_blog", "0006_alter_game_inning_part"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="inning_part",
            field=models.CharField(
                choices=[
                    ("pre-game", "game not started"),
                    ("top", "top"),
                    ("bottom", "bottom"),
                    ("final", "game concluded"),
                ],
                db_default=models.Value("pre-game"),
                max_length=10,
            ),
        ),
    ]
