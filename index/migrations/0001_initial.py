# Generated by Django 5.0.7 on 2024-07-14 01:25

import django.db.models.functions.datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrafficCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(max_length=128)),
                ('timestamp', models.DateTimeField(db_default=django.db.models.functions.datetime.Now())),
                ('ip', models.CharField(max_length=128, null=True)),
                ('user_agent', models.CharField(max_length=128, null=True)),
            ],
        ),
    ]
