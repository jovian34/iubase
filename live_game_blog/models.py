from django.db import models
from django.db.models.functions import Now

from live_game_blog.choices import INNING_PART_CHOICES, OUTS_CHOICES


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
    neutral_site = models.BooleanField(db_default=False)
    live_stats = models.URLField(null=True, blank=True)
    first_pitch = models.DateTimeField(null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.away_team.team_name} at {self.home_team.team_name} {self.first_pitch}"
    

class GameStatus(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    inning_num = models.IntegerField(db_default=1, null=False)
    inning_part = models.CharField(choices=INNING_PART_CHOICES, db_default="pre-game", max_length=10)
    outs = models.IntegerField(choices=OUTS_CHOICES, db_default=0)
    home_runs = models.IntegerField(null=False, db_default=0)
    away_runs = models.IntegerField(null=False, db_default=0)
    home_hits = models.IntegerField(null=False, db_default=0)
    away_hits = models.IntegerField(null=False, db_default=0)
    home_errors = models.IntegerField(null=False, db_default=0)
    away_errors = models.IntegerField(null=False, db_default=0)

    def __str__(self) -> str:
        return f"{self.game.away_team.name}-{self.away_runs}, {self.game.home_team.name}-{self.home_runs}, {self.inning_part} inning: {self.inning_num}"
    

    
class GameBlogEntry(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    blog_time = models.DateTimeField(db_default=Now())
    blog_entry = models.TextField()
    include_game_status = models.BooleanField(db_default=False)

    def __str__(self) -> str:
        return f"{self.blog_time}"


