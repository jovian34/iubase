from django import forms

from live_game_blog.models import Team, Stadium
from live_game_blog.choices import GAME_STATUS, INNING_PART_CHOICES, OUTS_CHOICES, TIMEZONE_CHOICES, SURFACE_CHOICES, DUGOUT_CHOICES


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

    def __init__(
            self, 
            *args, 
            label_away_runs=None,
            label_away_hits=None,
            label_away_errors=None,
            label_home_runs=None,
            label_home_hits=None,
            label_home_errors=None,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if label_away_runs:
            self.fields['away_runs'].label = label_away_runs
        if label_away_hits:
            self.fields['away_hits'].label = label_away_hits
        if label_away_errors:
            self.fields['away_errors'].label = label_away_errors
        if label_home_runs:
            self.fields['home_runs'].label = label_home_runs
        if label_home_hits:
            self.fields['home_hits'].label = label_home_hits
        if label_home_errors:
            self.fields['home_errors'].label = label_home_errors



class BlogEntryForm(forms.Form):
    is_raw_html = forms.BooleanField(label="Entry is RAW HTML code", required=False)
    is_photo_only = forms.BooleanField(label="Entry is photo URL only", required=False)
    is_x_embed = forms.BooleanField(
        label="Entry is @iubase17 X embed code", required=False
    )
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

    first_pitch = forms.DateTimeField(
        input_formats=["%Y-%m-%d-%H%M"],
        label="Date and Time of First Pitch YYYY-MM-DD-HHMM in ET military time",
    )
    event = forms.CharField(label="Describe the event: ", required=False)
    
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
    )
    live_stats = forms.URLField(
        label="Live Stats Link",
        required=False,
    )
    video = forms.CharField(
        label="Video Stream or TV provider",
        required=False,
    )
    video_url = forms.URLField(
        label="Video Stream or TV link",
        required=False,
    )
    audio_primary = forms.URLField(
        label="Primary Audio Link",
        required=False,
    )
    audio_student = forms.URLField(
        label="Student Audio Link",
        required=False,
    )
    

class AddNeutralGame(AddGameForm):
    stadium = forms.ModelChoiceField(
        queryset=Stadium.objects.all().order_by("address"),
        label="Stadium",
    )


class AddTeamForm(forms.Form):
    team_name = forms.CharField(label="Team Name")
    mascot = forms.CharField(label="Team Mascot")
    logo = forms.URLField(
        label="URL for the team's logo",
        required=False,
    )
    stats = forms.URLField(
        label="URL for the team's stats page",
        required=False,
    )
    roster = forms.URLField(
        label="URL for the team's roster page",
        required=False,
    )


class AddHomeStadiumDataForm(forms.Form):
    address = forms.CharField(label="Address")
    city = forms.CharField(label="City")
    state = forms.CharField(label="State")
    country = forms.CharField(label="Country")
    timezone = forms.ChoiceField(
        choices=TIMEZONE_CHOICES,
        label="Select Timezone",
    )
    lat = forms.DecimalField(label="Latitude")
    long = forms.DecimalField(label="Longitude")
    stadium_name = forms.CharField(label="Full name of the stadium")
    config_date = forms.DateField(label="Date stadium was set to this configuration (including name)")
    designate_date = forms.DateField(label="Date this configuration became exclusive home field")
    surface_inf = forms.ChoiceField(
        choices=SURFACE_CHOICES,
        label="Infield Surface",
    )
    surface_out = forms.ChoiceField(
        choices=SURFACE_CHOICES,
        label="Outfield Surface",
    )
    surface_mound = forms.ChoiceField(
        choices=SURFACE_CHOICES,
        label="Pitching Mound Surface",
    )
    photo = forms.URLField(
        label="Photo URL", 
        required=False,
    )
    orientation = forms.IntegerField(label="Out to centerfield orientation")
    left = forms.IntegerField(label="Distance from home to left field fence")
    center = forms.IntegerField(label="Distance from home to centerfield fence")
    right = forms.IntegerField(label="Distance from home to right field fence")
    capacity = forms.IntegerField(label="Fan Capacity")
    lights = forms.BooleanField(label="Does this stadium have working lights?")
    home_dugout = forms.ChoiceField(
        choices=DUGOUT_CHOICES,
        label="Which side is the home team dugout?"
    )
    