# Generated by Django 5.0 on 2024-01-15 22:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("player_tracking", "0006_rename_fall_year_annualroster_spring_year"),
    ]

    operations = [
        migrations.AlterField(
            model_name="annualroster",
            name="primary_position",
            field=models.CharField(
                choices=[
                    ("P", "Pitcher"),
                    ("C", "Catcher"),
                    ("1B", "First Base"),
                    ("2B", "Second Base"),
                    ("3B", "Third Base"),
                    ("SS", "Shortstop"),
                    ("CF", "Centerfield"),
                    ("OF", "Corner Outfield"),
                    ("DH", "Designated Hitter"),
                    (None, "None"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="annualroster",
            name="secondary_position",
            field=models.CharField(
                blank=True,
                choices=[
                    ("P", "Pitcher"),
                    ("C", "Catcher"),
                    ("1B", "First Base"),
                    ("2B", "Second Base"),
                    ("3B", "Third Base"),
                    ("SS", "Shortstop"),
                    ("CF", "Centerfield"),
                    ("OF", "Corner Outfield"),
                    ("DH", "Designated Hitter"),
                    (None, "None"),
                ],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="annualroster",
            name="status",
            field=models.CharField(
                choices=[
                    ("roster", "Spring Roster"),
                    ("waiver", "Played but granted eligibility waiver"),
                    ("redshirt", "On Spring Roster but did not play"),
                    ("greyshirt", "Not on Spring roster"),
                ],
                db_default=models.Value("roster"),
            ),
        ),
        migrations.AlterField(
            model_name="player",
            name="bats",
            field=models.CharField(
                blank=True,
                choices=[("left", "Left"), ("right", "Right"), ("both", "Both")],
                max_length=16,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="player",
            name="throws",
            field=models.CharField(
                blank=True,
                choices=[("left", "Left"), ("right", "Right"), ("both", "Both")],
                max_length=16,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="trans_event",
            field=models.CharField(
                choices=[
                    ("verbal", "Verbal Commitment from High School"),
                    ("transfer", "Verbal Commitment from College"),
                    ("nli", "National Letter of Intent Signed"),
                    ("decommit", "Decommit"),
                    ("in_portal", "Entered Transfer Portal"),
                    ("pro", "Signed Professional Contract"),
                    ("other", "No Longer With Program - Other Reason"),
                ],
                max_length=64,
            ),
        ),
    ]
