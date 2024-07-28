from django.db import models
from django.db.models.functions import Now

from live_game_blog.models import Team
from player_tracking.choices import (
    HAND_CHOICES,
    TRANSACTION_CHOICES,
    POSITION_CHOICES,
    STATUS_CHOICES,
)


class Player(models.Model):
    first = models.CharField(null=False, max_length=64)
    last = models.CharField(null=False, max_length=64)
    hsgrad_year = models.IntegerField(null=False)
    high_school = models.CharField(null=True, blank=True)
    home_city = models.CharField(null=True, blank=True)
    home_state = models.CharField(null=True, blank=True, max_length=8)
    home_country = models.CharField(db_default="USA")
    headshot = models.URLField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    primary_position = models.CharField(null=True, blank=True, choices=POSITION_CHOICES)
    bats = models.CharField(choices=HAND_CHOICES, max_length=16, null=True, blank=True)
    throws = models.CharField(
        choices=HAND_CHOICES, max_length=16, null=True, blank=True
    )
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)    
    first_spring = models.IntegerField(null=True, blank=True)
    last_spring = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.first} {self.last} {self.hsgrad_year}"


class ProfOrg(models.Model):
    city = models.CharField(null=True, blank=True)
    mascot = models.CharField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.city} {self.mascot}"


class Transaction(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    trans_event = models.CharField(choices=TRANSACTION_CHOICES, max_length=64)
    trans_date = models.DateField(db_default=Now())
    citation = models.URLField(null=True, blank=True)
    primary_position = models.CharField(null=True, blank=True, choices=POSITION_CHOICES)
    other_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    prof_org = models.ForeignKey(
        ProfOrg,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    draft_round = models.IntegerField(null=True, blank=True)
    bonus_or_slot = models.FloatField(null=True, blank=True)
    comment = models.CharField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.player.first} {self.player.last} {self.trans_event} on {self.trans_date:%B %Y}"
    


class AnnualRoster(models.Model):
    spring_year = models.IntegerField(null=False)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    jersey = models.IntegerField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, db_default="Fall Roster")
    primary_position = models.CharField(choices=POSITION_CHOICES)
    secondary_position = models.CharField(
        choices=POSITION_CHOICES, null=True, blank=True
    )

    def __str__(self) -> str:
        return (
            f"{self.player.first} {self.player.last} {self.spring_year} - {self.status}"
        )


class MLBDraftDate(models.Model):
    fall_year = models.IntegerField(null=False)
    latest_birthdate = models.DateField()
    latest_draft_day = models.DateField()
    signing_deadline = models.DateField()
    draft_complete = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.fall_year}: {self.latest_birthdate:%b %-d, %Y}"


class SummerLeague(models.Model):
    league = models.CharField(null=False, max_length=64)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.league


class SummerTeam(models.Model):
    name = models.CharField(null=False, max_length=64)
    mascot = models.CharField(null=False, max_length=64)
    website = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} {self.mascot}"


class SummerAssign(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    summer_year = models.IntegerField(null=False)
    summer_league = models.ForeignKey(SummerLeague, on_delete=models.CASCADE)
    summer_team = models.ForeignKey(SummerTeam, on_delete=models.CASCADE)
    source = models.CharField(null=True, blank=True)
    citation = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.player.first} {self.player.last} {self.summer_year} {self.summer_team.name}"