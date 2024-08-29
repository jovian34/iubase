# Generated by Django 5.0.6 on 2024-06-29 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("player_tracking", "0027_summerassign_citation_summerleague_url_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="summerleague",
            old_name="url",
            new_name="website",
        ),
        migrations.RenameField(
            model_name="summerteam",
            old_name="url",
            new_name="website",
        ),
        migrations.AddField(
            model_name="summerassign",
            name="source",
            field=models.CharField(blank=True, null=True),
        ),
    ]
