# Generated by Django 5.0.6 on 2024-06-01 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('live_game_blog', '0017_alter_game_neutral_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='home_seed',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
