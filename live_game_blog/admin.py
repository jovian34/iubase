from django.contrib import admin
from django.db import models
from live_game_blog.models import Game, Team, Scoreboard, BlogEntry


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    model = Team
    list_display = (
        "team_name",
        "mascot",
        "logo",
        "stats",
        "roster",
    )


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    model = Game
    list_display = (
        "home_team",
        "away_team",
        "neutral_site",
        "live_stats",
        "first_pitch",
    )


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
        "home_runs",
        "away_runs",
        "home_hits",
        "away_hits",
        "home_errors",
        "away_errors",
    )


@admin.register(BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    model = BlogEntry
    list_display = (
        "game",
        "author",
        "blog_time",
        "blog_entry",
        "include_scoreboard",
        "scoreboard",
    )