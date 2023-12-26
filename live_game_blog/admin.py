from django.contrib import admin
from django.db import models
from .models import Game, GameBlogEntry, Team


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



@admin.register(GameBlogEntry)
class GameBlogEntryAdmin(admin.ModelAdmin):
    model = GameBlogEntry
    list_display = (
        "game",
        "blog_time",
        "blog_entry",
        "include_game_status",
    )