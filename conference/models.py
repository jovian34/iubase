from django.db import models
from datetime import date

from live_game_blog import models as lgb_models
from accounts import models as acct_models


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
    

class ConfSeries(models.Model):
    home_team = models.ForeignKey(
        lgb_models.Team, 
        on_delete=models.CASCADE, 
        related_name="series_home_team",
    )
    away_team = models.ForeignKey(
        lgb_models.Team, 
        on_delete=models.CASCADE,
        related_name="series_away_team",
    )
    home_wins = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0,
    )
    away_wins = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0,
    )
    start_date = models.DateField()

    def __str__(self):
        return f"{self.away_team.team_name} at {self.home_team.team_name}: {self.start_date:%B} {self.start_date.day}-{self.start_date.day + 2}, {self.start_date.year}"
    

class TeamRpi(models.Model):
    team = models.ForeignKey(
        lgb_models.Team,
        on_delete=models.CASCADE,
    )
    rpi_rank = models.IntegerField()
    spring_year = models.IntegerField()

    def __str__(self):
        return f"{self.spring_year} {self.team.team_name}: {self.rpi_rank}"
    

class Pick(models.Model):
    user = models.ForeignKey(
        acct_models.CustomUser,
        on_delete=models.CASCADE,
    )
    series = models.ForeignKey(
        ConfSeries,
        on_delete=models.CASCADE,
    )
    pick = models.ForeignKey(
        lgb_models.Team,
        on_delete=models.CASCADE,
    )
    result = models.CharField(
        default="Incomplete",
    )

    def __str__(self):
        formatted_date = self.series.start_date.strftime("%B %-d, %Y")
        return f"{self.user.first_name} {self.user.last_name}: {formatted_date} - {self.pick.team_name} - {self.result}"
    