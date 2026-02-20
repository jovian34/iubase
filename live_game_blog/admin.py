from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from live_game_blog import models as lgb_models


@admin.register(lgb_models.Team)
class TeamAdmin(admin.ModelAdmin):
    model = lgb_models.Team
    list_display = ("team_name", "mascot")
    ordering = ["team_name"]
    search_fields = ("team_name",)


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

    # don't load the full FK objects for the admin widgets (fast for large tables)
    raw_id_fields = ("home_team", "away_team", "stadium_config")

    # for list view and change view header rendering (reduces queries)
    list_select_related = ("home_team", "away_team", "stadium_config")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # select_related reduces DB hits when admin accesses related team names (or in __str__)
        return qs.select_related("home_team", "away_team", "stadium_config")


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

    # use raw id fields to avoid loading full related rows into widgets
    raw_id_fields = ("game", "scorekeeper")

    # when showing Scoreboard rows, eagerly load the game and its teams to avoid nested queries
    list_select_related = ("game", "scorekeeper", "game__home_team", "game__away_team")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("game", "scorekeeper", "game__home_team", "game__away_team")


@admin.register(lgb_models.BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    model = lgb_models.BlogEntry
    list_display = ("game", "author", "blog_time", "include_scoreboard", "scoreboard")
    ordering = ["game", "-blog_time"]

    raw_id_fields = ("game", "author", "scoreboard")
    list_select_related = ("game", "author", "scoreboard", "game__home_team", "game__away_team")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("game", "author", "scoreboard", "game__home_team", "game__away_team")


@admin.register(lgb_models.Stadium)
class StadiumAdmin(admin.ModelAdmin):
    model = lgb_models.Stadium
    list_display = ("address", "city", "state")
    ordering = ["address"]
    search_fields = ("address", "city")


@admin.register(lgb_models.StadiumConfig)
class StadiumConfigAdmin(admin.ModelAdmin):
    model = lgb_models.StadiumConfig
    list_display = ("stadium_name", "config_date")
    ordering = ["stadium_name", "-config_date"]
    list_select_related = ("stadium",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("stadium")


@admin.register(lgb_models.HomeStadium)
class HomeStadiumAdmin(admin.ModelAdmin):
    model = lgb_models.HomeStadium
    list_display = ("team", "stadium_config", "designate_date")
    ordering = ["team", "-designate_date"]

    raw_id_fields = ("team", "stadium_config")
    list_select_related = ("team", "stadium_config")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("team", "stadium_config")