# Generated by Django 5.0 on 2024-01-16 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player_tracking', '0009_alter_player_birthdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='home_state',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]