# Generated by Django 5.0 on 2024-01-16 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player_tracking', '0008_alter_annualroster_primary_position_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
