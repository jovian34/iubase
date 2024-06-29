# Generated by Django 5.0.6 on 2024-06-07 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("player_tracking", "0018_remove_player_clock_player_last_spring"),
    ]

    operations = [
        migrations.AlterField(
            model_name="annualroster",
            name="status",
            field=models.CharField(
                choices=[
                    ("Fall Roster", "Fall Roster"),
                    ("Spring Roster", "Spring Roster"),
                    ("Not on Spring roster", "Not on Spring roster"),
                    (
                        "Played but granted eligibility waiver",
                        "Played but granted eligibility waiver",
                    ),
                    (
                        "On Spring Roster but did not play",
                        "On Spring Roster but did not play",
                    ),
                    (
                        "Replaced on Spring Roster - Medical",
                        "Replaced on Spring Roster - Medical",
                    ),
                ],
                db_default="Fall Roster",
            ),
        ),
        migrations.AlterField(
            model_name="player",
            name="last_spring",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
