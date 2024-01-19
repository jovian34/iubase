# Generated by Django 5.0.1 on 2024-01-19 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player_tracking', '0010_alter_player_home_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annualroster',
            name='status',
            field=models.CharField(choices=[('Fall Roster', 'Fall Roster'), ('Spring Roster', 'Spring Roster'), ('Played but granted eligibility waiver', 'Played but granted eligibility waiver'), ('On Spring Roster but did not play', 'On Spring Roster but did not play'), ('Not on Spring roster', 'Not on Spring roster')], db_default=models.Value('roster')),
        ),
    ]
