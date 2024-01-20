# Generated by Django 5.0.1 on 2024-01-14 04:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("player_tracking", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="annualroster",
            old_name="jersey_number",
            new_name="jersey",
        ),
        migrations.RemoveField(
            model_name="annualroster",
            name="granted_waiver",
        ),
        migrations.RemoveField(
            model_name="annualroster",
            name="grey_shirt",
        ),
        migrations.RemoveField(
            model_name="annualroster",
            name="played_in_spring",
        ),
        migrations.RemoveField(
            model_name="annualroster",
            name="spring_roster",
        ),
        migrations.AddField(
            model_name="annualroster",
            name="primary_position",
            field=models.CharField(
                choices=[
                    ("Pitcher", "P"),
                    ("Catcher", "C"),
                    ("First Base", "1B"),
                    ("Second Base", "2B"),
                    ("Third Base", "3B"),
                    ("Shortstop", "SS"),
                    ("Centerfield", "CF"),
                    ("Corner Outfield", "OF"),
                    ("Designated Hitter", "DH"),
                ],
                default="P",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="annualroster",
            name="secondary_position",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Pitcher", "P"),
                    ("Catcher", "C"),
                    ("First Base", "1B"),
                    ("Second Base", "2B"),
                    ("Third Base", "3B"),
                    ("Shortstop", "SS"),
                    ("Centerfield", "CF"),
                    ("Corner Outfield", "OF"),
                    ("Designated Hitter", "DH"),
                ],
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="annualroster",
            name="status",
            field=models.CharField(
                choices=[
                    ("Spring Roster", "roster"),
                    ("Played but granted eligibility waiver", "waiver"),
                    ("Roster not played", "redshirt"),
                    ("Not on Spring roster", "greyshirt"),
                ],
                db_default=models.Value("roster"),
            ),
        ),
    ]