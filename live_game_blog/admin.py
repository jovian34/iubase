from django.contrib import admin
from live_game_blog.models import Game, Team, Scoreboard, BlogEntry


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    model = Team
    list_display = (
        "team_name",
        "mascot",
    )


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    model = Game
    list_display = (
        "home_team",
        "away_team",
        "event",
        "neutral_site",
        "first_pitch",
    )
    ordering = ["-first_pitch"]


@admin.register(Scoreboard)
class ScoreboardAdmin(admin.ModelAdmin):
    model = Scoreboard
    list_display = (
        "game",
        "scorekeeper",
        "update_time",
        "game_status",
        "inning_num",
        "inning_part",
        "outs",
    )
    ordering = ["-update_time"]


@admin.register(BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    model = BlogEntry
    list_display = (
        "game",
        "author",
        "blog_time",
        "include_scoreboard",
        "scoreboard",
    )
    ordering = ["game", "-blog_time"]
