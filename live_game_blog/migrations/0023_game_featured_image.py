# Generated by Django 5.1.3 on 2024-12-13 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('live_game_blog', '0022_remove_game_fall_exhibition'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='featured_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
