# Generated by Django 5.0.6 on 2024-05-30 17:14

import django.db.models.functions.datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("player_tracking", "0014_alter_transaction_trans_event"),
    ]

    operations = [
        migrations.AlterField(
            model_name="annualroster",
            name="status",
            field=models.CharField(
                choices=[
                    ("Fall Roster", "Fall Roster"),
                    ("Spring Roster", "Spring Roster"),
                    (
                        "Played but granted eligibility waiver",
                        "Played but granted eligibility waiver",
                    ),
                    (
                        "On Spring Roster but did not play",
                        "On Spring Roster but did not play",
                    ),
                    ("Not on Spring roster", "Not on Spring roster"),
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
            name="clock",
            field=models.IntegerField(db_default=5),
        ),
        migrations.AlterField(
            model_name="player",
            name="home_country",
            field=models.CharField(db_default="USA"),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="trans_date",
            field=models.DateField(
                db_default=django.db.models.functions.datetime.Now()
            ),
        ),
    ]
