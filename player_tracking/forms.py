from django import forms
from django.db import models

from player_tracking.models import Player, Transaction, AnnualRoster
from live_game_blog.models import Team
from player_tracking.choices import (
    HAND_CHOICES,
    TRANSACTION_CHOICES,
    POSITION_CHOICES,
    STATUS_CHOICES,
)

class NewPlayerForm(forms.Form):
    first = forms.CharField(label="First Name")
    last = forms.CharField(label="Last Name")
    hsgrad_year = forms.IntegerField(label="High School Graduate Year")
    high_school = forms.CharField(label="High School")
    home_city = forms.CharField(label="Home City")
    home_state = forms.CharField(label="Home State", required=False)
    home_country = forms.CharField(label="Home Country")
    headshot = forms.URLField(
        label="Headshot or other photo file URL",
        required=False,
        assume_scheme="https",  # remove argument for Django 6.0
    )
    birthdate = forms.DateField(label="Date of Birth", required=False)
    bats = forms.ChoiceField(
        label="Batting hand",
        choices=HAND_CHOICES,
        required=False,
    )
    throws = forms.ChoiceField(
        label="Throwing hand",
        choices=HAND_CHOICES,
        required=False,
    )
    height = forms.IntegerField(label="height in Inches", required=False)
    weight = forms.IntegerField(label="Weight in Lbs.", required=False)
    clock = forms.IntegerField(label="Years to complete eligibility - almost always 5")


class AnnualRosterForm(forms.Form):
    spring_year = forms.IntegerField(label="Spring Year")
    team = forms.ModelChoiceField(
        queryset=Team.objects.all().order_by("team_name"),
        label="Team",
    )
    jersey = forms.IntegerField(label="Jersey Number", required=False)
    status = forms.ChoiceField(label="Eligibility Status", choices=STATUS_CHOICES)
    primary_position = forms.ChoiceField(label="Primary Fielding Position", choices=POSITION_CHOICES)
    secondary_position = forms.ChoiceField(label="Secondary Fielding Position", choices=POSITION_CHOICES, required=False)