# Generated by Django 5.0 on 2023-12-27 21:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("live_game_blog", "0007_alter_game_inning_part"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="game",
            name="away_errors",
        ),
        migrations.RemoveField(
            model_name="game",
            name="away_hits",
        ),
        migrations.RemoveField(
            model_name="game",
            name="away_runs",
        ),
        migrations.RemoveField(
            model_name="game",
            name="home_errors",
        ),
        migrations.RemoveField(
            model_name="game",
            name="home_hits",
        ),
        migrations.RemoveField(
            model_name="game",
            name="home_runs",
        ),
        migrations.RemoveField(
            model_name="game",
            name="inning_num",
        ),
        migrations.RemoveField(
            model_name="game",
            name="inning_part",
        ),
        migrations.RemoveField(
            model_name="game",
            name="outs",
        ),
        migrations.CreateModel(
            name="GameStatus",
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
                ("inning_num", models.IntegerField(db_default=models.Value(1))),
                (
                    "inning_part",
                    models.CharField(
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
                (
                    "outs",
                    models.IntegerField(
                        choices=[(0, "none"), (1, "one"), (2, "two"), (3, "three")],
                        db_default=models.Value(0),
                    ),
                ),
                ("home_runs", models.IntegerField(db_default=models.Value(0))),
                ("away_runs", models.IntegerField(db_default=models.Value(0))),
                ("home_hits", models.IntegerField(db_default=models.Value(0))),
                ("away_hits", models.IntegerField(db_default=models.Value(0))),
                ("home_errors", models.IntegerField(db_default=models.Value(0))),
                ("away_errors", models.IntegerField(db_default=models.Value(0))),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="live_game_blog.game",
                    ),
                ),
            ],
        ),
    ]
