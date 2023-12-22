from django import forms
from django.db import models

from live_game_blog.models import Scoreboard, BlogEntry
from live_game_blog.choices import GAME_STATUS, INNING_PART_CHOICES, OUTS_CHOICES


class BlogAndScoreboardForm(forms.Form):
    game_status = forms.ChoiceField(label="Game status", choices=GAME_STATUS)
    inning_num = forms.IntegerField(label="Inning")
    inning_part = forms.ChoiceField(label="Top/Bottom", choices=INNING_PART_CHOICES)
    outs = forms.ChoiceField(label="Outs", choices=OUTS_CHOICES)
    home_runs = forms.IntegerField(label="Home Team Runs Scored")
    away_runs = forms.IntegerField(label="Away Team Runs Scored")
    home_hits = forms.IntegerField(label="Home Team Hits")
    away_hits = forms.IntegerField(label="Away Team Hits")
    home_errors = forms.IntegerField(label="Home Team Errors")
    away_errors = forms.IntegerField(label="Away Team Errors")
    blog_entry = forms.CharField(label="Content of Blog", widget=forms.Textarea())

class BlogEntryForm(forms.Form):
    blog_entry = forms.CharField(label="Content of Blog", widget=forms.Textarea())