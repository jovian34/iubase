# Generated by Django 5.0.7 on 2024-07-14 23:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("index", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trafficcounter",
            name="ip",
            field=models.CharField(max_length=256, null=True),
        ),
    ]
