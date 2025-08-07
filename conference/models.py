from django.db import models
from datetime import date

from live_game_blog import models as lgb_models


class Conference(models.Model):
    abbrev = models.CharField(null=False, max_length=8, unique=True)
    long_name = models.CharField(null=False, max_length=64, unique=True)
    logo_url = models.URLField(null=True, max_length=256)

    def __str__(self):
        return self.abbrev    


class ConfTeam(models.Model):
    team = models.ForeignKey(
        lgb_models.Team, on_delete=models.CASCADE, 
    )
    conference = models.ForeignKey(
        Conference, on_delete=models.CASCADE,
    )
    fall_year_joined = models.IntegerField(
        null=False, default=date.today().year
    )

    def __str__(self):
        return f"{self.team.team_name} - {self.conference.abbrev}"
    