from django import forms
from django.db import models

from live_game_blog.models import Scoreboard, BlogEntry, Game, Team
from live_game_blog.choices import GAME_STATUS, INNING_PART_CHOICES, OUTS_CHOICES


class BlogAndScoreboardForm(forms.Form):
    game_status = forms.ChoiceField(label="Game status", choices=GAME_STATUS)
    inning_num = forms.IntegerField(label="Inning")
    inning_part = forms.ChoiceField(label="Top/Bottom", choices=INNING_PART_CHOICES)
    outs = forms.ChoiceField(label="Outs", choices=OUTS_CHOICES)
    away_runs = forms.IntegerField(label="Away Team Runs Scored")
    home_runs = forms.IntegerField(label="Home Team Runs Scored")
    away_hits = forms.IntegerField(label="Away Team Hits")
    home_hits = forms.IntegerField(label="Home Team Hits")
    away_errors = forms.IntegerField(label="Away Team Errors")
    home_errors = forms.IntegerField(label="Home Team Errors")
    blog_entry = forms.CharField(label="Content of Blog", widget=forms.Textarea())

class BlogEntryForm(forms.Form):
    is_raw_html = forms.BooleanField(label="Entry is RAW HTML code", required=False)
    is_x_embed = forms.BooleanField(label="Entry is @iubase17 X embed code", required=False)
    blog_entry = forms.CharField(label="Content of Blog", widget=forms.Textarea())
    
class AddGameForm(forms.Form):
    home_team = forms.ModelChoiceField(
        queryset=Team.objects.all().order_by("team_name"),
        label="Home Team",
    )
    away_team = forms.ModelChoiceField(
        queryset=Team.objects.all().order_by("team_name"),
        label="Away Team",
    )
    neutral_site = forms.BooleanField(label="Is this a neutral site or host is designated away?", required=False)
    live_stats = forms.URLField(label="Live Stats Link", required=False)
    first_pitch = forms.DateTimeField(input_formats=['%Y-%m-%d-%H%M'], label="Date and Time of First Pitch YYYY-MM-DD-HHMM in military time")