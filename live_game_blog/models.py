from django.db import models
from django.db.models.functions import Now

from live_game_blog.choices import INNING_PART_CHOICES, OUTS_CHOICES, GAME_STATUS
from accounts.models import CustomUser


class Team(models.Model):
    team_name = models.CharField(null=False, max_length=64, unique=True)
    mascot = models.CharField(null=False, max_length=64)
    logo = models.URLField()
    stats = models.URLField()
    roster = models.URLField()

    def __str__(self) -> str:
        return self.team_name
    

class Stadium(models.Model):
    address = models.CharField(null=False, max_length=128)
    city = models.CharField(null=False, max_length=64)
    state = models.CharField(null=True, blank=True, max_length=2)
    country = models.CharField(null=False, max_length=64)
    timezone = models.CharField(null=False, max_length=64)
    lat = models.DecimalField(decimal_places=14, max_digits=32)
    long = models.DecimalField(decimal_places=14, max_digits=32)

    def __str__(self):
        return f"{self.address} | {self.city}, {self.state} {self.country}"


class Game(models.Model):
    home_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="home_team_set"
    )
    home_rank = models.IntegerField(null=True, blank=True)
    home_seed = models.IntegerField(null=True, blank=True)
    home_nat_seed = models.IntegerField(null=True, blank=True)
    away_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="away_team_set"
    )
    away_rank = models.IntegerField(null=True, blank=True)
    away_seed = models.IntegerField(null=True, blank=True)
    away_nat_seed = models.IntegerField(null=True, blank=True)

    neutral_site = models.BooleanField(db_default=False)
    event = models.CharField(null=True, blank=True)
    featured_image = models.URLField(null=True, blank=True)
    live_stats = models.URLField(null=True, blank=True)
    first_pitch = models.DateTimeField(null=True, blank=True)
    video = models.CharField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    audio_primary = models.URLField(null=True, blank=True)
    audio_student = models.URLField(null=True, blank=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, null=True, blank=True)
    first_pitch_temp = models.DecimalField(max_digits=8, decimal_places=1, null=True, blank=True)
    first_pitch_feels_like = models.DecimalField(max_digits=8, decimal_places=1, null=True, blank=True)
    first_pitch_wind_speed = models.DecimalField(max_digits=8, decimal_places=1, null=True, blank=True)
    first_pitch_wind_angle = models.IntegerField(null=True, blank=True)
    first_pitch_wind_gusts = models.DecimalField(max_digits=8, decimal_places=1, null=True, blank=True)
    first_pitch_weather_describe = models.CharField(max_length=128, null=True, blank=True)
    gameday_sunset = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        vs = "at"
        if self.neutral_site:
            vs = "vs."
        return f"{self.first_pitch:%Y-%m-%d %H:%M} UTC - {self.away_team.team_name} {vs} {self.home_team.team_name}"


class Scoreboard(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    scorekeeper = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    update_time = models.DateTimeField(db_default=Now())
    game_status = models.CharField(choices=GAME_STATUS, max_length=16)
    inning_num = models.IntegerField(null=True, blank=True)
    inning_part = models.CharField(
        choices=INNING_PART_CHOICES, max_length=16, null=True, blank=True
    )
    outs = models.IntegerField(choices=OUTS_CHOICES, null=True, blank=True)
    home_runs = models.IntegerField(null=True, blank=True)
    away_runs = models.IntegerField(null=True, blank=True)
    home_hits = models.IntegerField(null=True, blank=True)
    away_hits = models.IntegerField(null=True, blank=True)
    home_errors = models.IntegerField(null=True, blank=True)
    away_errors = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        home_team = self.game.home_team.team_name
        away_team = self.game.away_team.team_name
        return f"{away_team}-{self.away_runs}, {home_team}-{self.home_runs} | {self.inning_part} Inning: {self.inning_num}"


class BlogEntry(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog_time = models.DateTimeField(db_default=Now())
    blog_entry = models.TextField()
    is_raw_html = models.BooleanField(null=True, blank=True)
    is_photo_only = models.BooleanField(null=True, blank=True)
    include_scoreboard = models.BooleanField()
    scoreboard = models.ForeignKey(
        Scoreboard, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.author}: {self.blog_time}"
    

class StadiumConfig(models.Model):
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    stadium_name = models.CharField(null=False, max_length=128)
    config_date = models.DateField(null=False)
    surface_inf = models.CharField(null=True, blank=True, max_length=16)
    surface_out = models.CharField(null=True, blank=True, max_length=16)
    surface_mound = models.CharField(null=True, blank=True, max_length=16)
    photo = models.URLField(null=True, blank=True)
    orientation = models.IntegerField(null=False)
    left = models.IntegerField(null=True, blank=True)
    center = models.IntegerField(null=True, blank=True)
    right = models.IntegerField(null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    lights = models.BooleanField(default=True)
    home_dugout = models.CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.stadium_name} - {self.config_date.year}"
    

class HomeStadium(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    stadium_config = models.ForeignKey(StadiumConfig, on_delete=models.CASCADE)
    designate_date = models.DateField(null=False)

    def __str__(self):
        return f"{self.team}: {self.stadium_config.stadium_name} - {self.designate_date.year}"

