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
    )



@admin.register(GameBlogEntry)
class GameBlogEntryAdmin(admin.ModelAdmin):
    model = GameBlogEntry
    list_display = (
        "game",
        "blog_time",
        "inning_num",
        "inning_part",
        "outs",
    )