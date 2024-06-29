# Generated by Django 5.0.6 on 2024-06-08 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player_tracking', '0021_mlbdraftdate_latest_draft_day_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='primary_position',
            field=models.CharField(blank=True, choices=[('Pitcher', 'Pitcher'), ('Catcher', 'Catcher'), ('First Base', 'First Base'), ('Second Base', 'Second Base'), ('Third Base', 'Third Base'), ('Shortstop', 'Shortstop'), ('Centerfield', 'Centerfield'), ('Corner Outfield', 'Corner Outfield'), ('Designated Hitter', 'Designated Hitter'), (None, 'None')], null=True),
        ),
    ]