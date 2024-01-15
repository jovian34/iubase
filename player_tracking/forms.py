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