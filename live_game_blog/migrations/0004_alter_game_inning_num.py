# Generated by Django 5.0 on 2023-12-27 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('live_game_blog', '0003_remove_gameblogentry_away_errors_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='inning_num',
            field=models.IntegerField(db_default=models.Value(1)),
        ),
    ]
