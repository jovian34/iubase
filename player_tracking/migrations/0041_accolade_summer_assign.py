# Generated by Django 5.1.4 on 2024-12-26 01:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player_tracking', '0040_alter_accolade_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='accolade',
            name='summer_assign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='player_tracking.summerassign'),
        ),
    ]