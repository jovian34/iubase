from django.db import models
from django.utils import timezone

class Team(models.Model):
    team_name = models.CharField(null=False, max_length=64)
    mascot = models.CharField(null=False, max_length=64)
    logo = models.URLField()
    stats = models.URLField()
    roster = models.URLField()

    def __str__(self) -> str:
        return self.team_name
    
class Game(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_team_set")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_team_set")
    neutral_site = models.BooleanField(default=False)
    live_stats = models.URLField()
    first_pitch = models.DateTimeField()
    
    def __str__(self) -> str:
        return f"{self.away_team.team_name} at {self.home_team.team_name} {self.first_pitch}"
    
class GameBlogEntry(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    blog_time = models.DateTimeField(default=timezone.now)
    inning_num = models.IntegerField()
    inning_part = models.CharField(null=False, max_length=16)
    outs = models.IntegerField()
    home_runs = models.IntegerField()
    away_runs = models.IntegerField()
    home_hits = models.IntegerField()
    away_hits = models.IntegerField()
    home_errors = models.IntegerField()
    away_errors = models.IntegerField()
    blog_entry = models.TextField()

    def __str__(self) -> str:
        return f"{self.away_runs}-{self.home_runs} {self.inning_part}-{self.inning_num}"


