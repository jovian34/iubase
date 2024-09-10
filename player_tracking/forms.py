from django import forms
from player_tracking import models as pt_models
from live_game_blog import models as lgb_models
from player_tracking import choices


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
        choices=choices.HAND_CHOICES,
        required=False,
    )
    throws = forms.ChoiceField(
        label="Throwing hand",
        choices=choices.HAND_CHOICES,
        required=False,
    )
    height = forms.IntegerField(label="height in Inches", required=False)
    weight = forms.IntegerField(label="Weight in Lbs.", required=False)
    trans_event = forms.ChoiceField(
        label="Transaction",
        choices=choices.TRANSACTION_CHOICES,
        required=True,
    )
    trans_date = forms.DateField(label="Transaction Date")
    citation = forms.CharField(label="Citation", required=False)
    primary_position = forms.ChoiceField(
        label="Primary Position",
        choices=choices.POSITION_CHOICES,
    )


class AnnualRosterForm(forms.Form):
    spring_year = forms.IntegerField(label="Spring Year")
    team = forms.ModelChoiceField(
        queryset=lgb_models.Team.objects.all().order_by("team_name"),
        label="Team",
    )
    jersey = forms.IntegerField(label="Jersey Number", required=False)
    status = forms.ChoiceField(label="Eligibility Status", choices=choices.STATUS_CHOICES)
    primary_position = forms.ChoiceField(
        label="Primary Fielding Position", choices=choices.POSITION_CHOICES
    )
    secondary_position = forms.ChoiceField(
        label="Secondary Fielding Position", choices=choices.POSITION_CHOICES, required=False
    )


class TransactionForm(forms.Form):
    trans_event = forms.ChoiceField(
        label="Transaction Event",
        choices=choices.TRANSACTION_CHOICES,
    )
    trans_date = forms.DateField(label="Transaction Date")
    citation = forms.CharField(label="Citation", required=False)
    primary_position = forms.ChoiceField(
        label="Primary Position",
        choices=choices.POSITION_CHOICES,
        required=False,
    )
    other_team = forms.ModelChoiceField(
        queryset=lgb_models.Team.objects.all().order_by("team_name"),
        label="Transfer College",
        required=False,
    )
    prof_org = forms.ModelChoiceField(
        queryset=pt_models.ProfOrg.objects.all().order_by("city"),
        label="MLB Program",
        required=False,
    )
    draft_round = forms.IntegerField(
        label="Draft Rounds - number only ex: 4C is just 4",
        required=False,
    )
    bonus_or_slot = forms.FloatField(
        label="Bonus awarded for signing or value of the slot if drafted",
        required=False,
    )
    comment = forms.CharField(
        label="Extra information about this transaction in one complete sentence",
        required=False,
    )


class SummerAssignForm(forms.Form):
    summer_year = forms.IntegerField(label="Summer Year")
    summer_league = forms.ModelChoiceField(
        queryset=pt_models.SummerLeague.objects.all().order_by("league"),
        label="League",
    )
    summer_team = forms.ModelChoiceField(
        queryset=pt_models.SummerTeam.objects.all().order_by("name"), label="Summer Team"
    )
    source = forms.CharField(required=False, label="Source")
    citation = forms.URLField(
        required=False,
        label="Citation",
        assume_scheme="https",  # remove argument for Django 6.0
    )
