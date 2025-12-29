from django import forms

from conference import models as conf_models
from live_game_blog import models as lgb_models
from conference.views import conf_year


class AddConferenceSeriesForm(forms.Form):
    start_date = forms.DateField(label="Series start date")
    home_team = forms.ModelChoiceField(
        queryset=lgb_models.Team.objects.all(),
        label="Home Team",
    )
    away_team = forms.ModelChoiceField(
        queryset=lgb_models.Team.objects.all(),
        label="Away Team",
    )


    def __init__(self, *args, **kwargs):
        spring_year = kwargs.pop("spring_year")
        conference = conf_models.Conference.objects.get(abbrev="B1G")
        all_conf_teams = conf_models.ConfTeam.objects.filter(conference=conference)
        this_conf_teams = conf_year.get_conf_teams_for_requested_year(spring_year, conference, all_conf_teams)
        pks = [ team.pk for team in this_conf_teams ]
        super(AddConferenceSeriesForm, self).__init__(*args, **kwargs)
        self.fields["home_team"].queryset = lgb_models.Team.objects.filter(pk__in=pks).order_by("team_name")
        self.fields["away_team"].queryset = lgb_models.Team.objects.filter(pk__in=pks).order_by("team_name")