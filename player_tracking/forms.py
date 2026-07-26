from django import forms
from django.db.models import Q

from live_game_blog import models as lgb_models
from player_tracking import choices
from player_tracking import models as pt_models


class PlayerForm(forms.Form):
    first = forms.CharField(label="First Name")
    last = forms.CharField(label="Last Name")
    hsgrad_year = forms.IntegerField(label="High School Graduate Year")
    high_school = forms.CharField(label="High School")
    home_city = forms.CharField(label="Home City")
    home_state = forms.CharField(label="Home State", required=False)
    home_country = forms.CharField(label="Home Country")
    headshot = forms.URLField(
        label="Portrait headshot URL",
        required=False,
    )
    action_shot = forms.URLField(
        label="Landscape action shot URL",
        required=False,
    )
    birthdate = forms.DateField(label="Date of Birth", required=False)
    bats = forms.ChoiceField(
        label="Batting hand",
        choices=choices.HAND,
        required=False,
    )
    throws = forms.ChoiceField(
        label="Throwing hand",
        choices=choices.HAND,
        required=False,
    )
    height = forms.IntegerField(label="height in Inches", required=False)
    weight = forms.IntegerField(label="Weight in Lbs.", required=False)
    primary_position = forms.ChoiceField(
        label="Primary Position",
        choices=choices.POSITIONS,
        required=False,
    )
    transfer_school = forms.ModelChoiceField(
        queryset=lgb_models.Team.objects.all().order_by("team_name"),
        required=False,
        label="Transfer School",
    )


class NewPlayerForm(PlayerForm):
    trans_event = forms.ChoiceField(
        label="Transaction",
        choices=choices.TRANSACTIONS,
        required=True,
    )
    trans_date = forms.DateField(label="Transaction Date")
    citation = forms.CharField(label="Citation", required=False)


class AnnualRosterForm(forms.Form):
    spring_year = forms.IntegerField(label="Spring Year")
    team = forms.ModelChoiceField(
        queryset=lgb_models.Team.objects.all().order_by("team_name"),
        label="Team",
    )
    jersey = forms.IntegerField(label="Jersey Number", required=False)
    status = forms.ChoiceField(
        label="Eligibility Status", choices=choices.STATUS_CHOICES
    )
    primary_position = forms.ChoiceField(
        label="Primary Fielding Position", choices=choices.POSITIONS
    )
    secondary_position = forms.ChoiceField(
        label="Secondary Fielding Position", choices=choices.POSITIONS, required=False
    )


class TransactionForm(forms.Form):
    trans_event = forms.ChoiceField(
        label="Transaction Event",
        choices=choices.TRANSACTIONS,
    )
    trans_date = forms.DateField(label="Transaction Date")
    citation = forms.CharField(label="Citation", required=False)
    primary_position = forms.ChoiceField(
        label="Primary Position",
        choices=choices.POSITIONS,
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
        queryset=pt_models.SummerTeam.objects.all().order_by("name"),
        label="Summer Team",
    )
    source = forms.CharField(required=False, label="Source")
    citation = forms.URLField(
        required=False,
        label="Citation",
    )


class AccoladeForm(forms.Form):
    def __init__(self, *args, player_id, **kwargs):
        self.player_id = int(player_id)
        super().__init__(*args, **kwargs)
        self.fields["annual_roster"].queryset = pt_models.AnnualRoster.objects.filter(
            player=self.player_id
        )
        self.fields["summer_assign"].queryset = pt_models.SummerAssign.objects.filter(
            player=self.player_id
        )

    name = forms.CharField(label="Name of accolade")
    award_date = forms.DateField(label="Date issued")
    award_org = forms.CharField(
        label="Sponsor Organization",
    )
    description = forms.CharField(
        label="Detailed description",
        required=False,
    )
    citation = forms.URLField(
        label="Web link for announcement",
    )
    annual_roster = forms.ModelChoiceField(
        queryset=pt_models.AnnualRoster.objects.all(),
        label="Applicable college roster",
        required=False,
    )
    summer_assign = forms.ModelChoiceField(
        queryset=pt_models.SummerAssign.objects.all(),
        label="Applicable summer assignment",
        required=False,
    )


class RosterPlayerChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, roster):
        return f"{roster.player.first} {roster.player.last}"


class RedBeltEntryForm(forms.Form):
    award_date = forms.DateField(
        label="Award Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    pitcher = RosterPlayerChoiceField(
        queryset=pt_models.AnnualRoster.objects.none(),
        label="Joey DeNato Weekly Red Belt for pitching",
    )
    hitter = RosterPlayerChoiceField(
        queryset=pt_models.AnnualRoster.objects.none(),
        label="Alex Dickerson Weekly Red Belt for hitting",
    )
    defender = RosterPlayerChoiceField(
        queryset=pt_models.AnnualRoster.objects.none(),
        label="Tony Butler Weekly Red Belt for defense",
    )

    def __init__(self, *args, spring_year, **kwargs):
        self.spring_year = int(spring_year)
        super().__init__(*args, **kwargs)
        roster = (
            pt_models.AnnualRoster.objects.filter(
                spring_year=self.spring_year,
                team__team_name="Indiana",
                status__in=choices.ALL_ROSTER,
            )
            .select_related("player")
            .order_by("player__last", "player__first")
        )
        self.fields["pitcher"].queryset = roster.filter(
            Q(primary_position="Pitcher") | Q(secondary_position="Pitcher")
        )
        self.fields["hitter"].queryset = roster
        self.fields["defender"].queryset = roster

    def clean_award_date(self):
        award_date = self.cleaned_data["award_date"]
        if award_date.year != self.spring_year:
            raise forms.ValidationError(
                f"The award date must be in {self.spring_year}."
            )
        return award_date
