# Generated by Django 5.0.6 on 2024-05-30 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('live_game_blog', '0016_alter_scoreboard_inning_part'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='neutral_site',
            field=models.BooleanField(db_default=False),
        ),
    ]
