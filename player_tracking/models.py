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
    home_state = models.CharField(max_length=2, null=True, blank=True)
    home_country = models.CharField(db_default="USA")
    headshot = models.URLField(null=True, blank=True)
    birthdate = models.DateTimeField(null=True, blank=True)
    bats = models.CharField(choices=HAND_CHOICES, max_length=16, null=True, blank=True)
    throws = models.CharField(
        choices=HAND_CHOICES, max_length=16, null=True, blank=True
    )
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    clock = models.IntegerField(db_default=5)

    def __str__(self) -> str:
        return f"{self.first} {self.last} {self.hsgrad_year}"


class Transaction(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    trans_event = models.CharField(choices=TRANSACTION_CHOICES, max_length=64)
    trans_date = models.DateTimeField(db_default=Now())
    citation = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.player.first} {self.player.last} {self.trans_event} on {self.trans_date:%B %Y}"


class AnnualRoster(models.Model):
    fall_year = models.IntegerField(null=False)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    jersey = models.IntegerField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, db_default="roster")
    primary_position = models.CharField(choices=POSITION_CHOICES)
    secondary_position = models.CharField(
        choices=POSITION_CHOICES, null=True, blank=True
    )

    def __str__(self) -> str:
        return (
            f"{self.player.first} {self.player.last} {self.fall_year} - {self.status}"
        )
