# Generated by Django 5.0.6 on 2024-06-03 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player_tracking', '0015_alter_annualroster_status_alter_player_clock_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MLBDraftDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fall_year', models.IntegerField()),
                ('latest_birthdate', models.DateField()),
            ],
        ),
    ]