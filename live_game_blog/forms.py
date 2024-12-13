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
    away_hits = forms.IntegerField(label="Away Team Hits")
    away_errors = forms.IntegerField(label="Away Team Errors")
    home_runs = forms.IntegerField(label="Home Team Runs Scored")
    home_hits = forms.IntegerField(label="Home Team Hits")
    home_errors = forms.IntegerField(label="Home Team Errors")
    blog_entry = forms.CharField(label="Content of Blog", widget=forms.Textarea())


class BlogEntryForm(forms.Form):
    is_raw_html = forms.BooleanField(label="Entry is RAW HTML code", required=False)
    is_x_embed = forms.BooleanField(
        label="Entry is @iubase17 X embed code", required=False
    )
    blog_entry = forms.CharField(label="Content of Blog", widget=forms.Textarea())


class AddGameForm(forms.Form):
    first_pitch = forms.DateTimeField(
        input_formats=["%Y-%m-%d-%H%M"],
        label="Date and Time of First Pitch YYYY-MM-DD-HHMM in ET military time",
    )
    neutral_site = forms.BooleanField(
        label="Is this a neutral site or host is designated away?", required=False
    )
    event = forms.CharField(
        label="Describe the event: ", required=False
    )

    home_team = forms.ModelChoiceField(
        queryset=Team.objects.all().order_by("team_name"),
        label="Home Team",
    )
    home_rank = forms.IntegerField(
        label="Home team D1Baseball.com national ranking",
        required=False,
    )
    home_seed = forms.IntegerField(
        label="Home team tournament seed",
        required=False,
    )
    home_nat_seed = forms.IntegerField(
        label="Home team national tournament seed",
        required=False,
    )

    away_team = forms.ModelChoiceField(
        queryset=Team.objects.all().order_by("team_name"),
        label="Away Team",
    )
    away_rank = forms.IntegerField(
        label="Away team D1Baseball.com national ranking",
        required=False,
    )
    away_seed = forms.IntegerField(
        label="Away team tournament seed",
        required=False,
    )
    away_nat_seed = forms.IntegerField(
        label="Away team national tournament seed",
        required=False,
    )
    featured_image = forms.URLField(
        label="Featured Image",
        required=False,
        assume_scheme="https",  # remove argument for Django 6.0
    )
    live_stats = forms.URLField(
        label="Live Stats Link",
        required=False,
        assume_scheme="https",  # remove argument for Django 6.0
    )
    video = forms.CharField(
        label="Video Stream or TV provider",
        required=False,
    )
    video_url = forms.URLField(
        label="Video Stream or TV link",
        required=False,
        assume_scheme="https",  # remove argument for Django 6.0
    )
    audio_primary = forms.URLField(
        label="Primary Audio Link",
        required=False,
        assume_scheme="https",  # remove argument for Django 6.0
    )
    audio_student = forms.URLField(
        label="Student Audio Link",
        required=False,
        assume_scheme="https",  # remove argument for Django 6.0
    )


class AddTeamForm(forms.Form):
    team_name = forms.CharField(label="Team Name")
    mascot = forms.CharField(label="Team Mascot")
    logo = forms.URLField(
        label="URL for the team's logo",
        required=False,
        assume_scheme="https",  # remove argument for Django 6.0
    )
    stats = forms.URLField(
        label="URL for the team's stats page",
        required=False,
        assume_scheme="https",  # remove argument for Django 6.0
    )
    roster = forms.URLField(
        label="URL for the team's roster page",
        required=False,
        assume_scheme="https",  # remove argument for Django 6.0
    )
