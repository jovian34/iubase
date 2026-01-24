from django.contrib import admin
from live_game_blog import models as lgb_models


@admin.register(lgb_models.Team)
class TeamAdmin(admin.ModelAdmin):
    model = lgb_models.Team
    list_display = (
        "team_name",
        "mascot",
    )
    ordering = ["team_name"]


@admin.register(lgb_models.Game)
class GameAdmin(admin.ModelAdmin):
    model = lgb_models.Game
    list_display = (
        "home_team",
        "away_team",
        "event",
        "neutral_site",
        "first_pitch",
    )
    ordering = ["-first_pitch"]


@admin.register(lgb_models.Scoreboard)
class ScoreboardAdmin(admin.ModelAdmin):
    model = lgb_models.Scoreboard
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


@admin.register(lgb_models.BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    model = lgb_models.BlogEntry
    list_display = (
        "game",
        "author",
        "blog_time",
        "include_scoreboard",
        "scoreboard",
    )
    ordering = ["game", "-blog_time"]


@admin.register(lgb_models.Stadium)
class StadiumAdmin(admin.ModelAdmin):
    model = lgb_models.Stadium
    list_display = (
        "address",
        "city",
        "state",
    )
    ordering = ["address"]


@admin.register(lgb_models.StadiumConfig)
class StadiumConfigAdmin(admin.ModelAdmin):
    model = lgb_models.Stadium
    list_display = (
        "stadium_name",
        "config_date",
    )
    ordering = ["stadium_name", "-config_date"]


@admin.register(lgb_models.HomeStadium)
class HomeStadiumAdmin(admin.ModelAdmin):
    model = lgb_models.HomeStadium
    list_display = (
        "team",
        "stadium_config",
        "designate_date",
    )
    ordering = ["team", "-designate_date"]
