from django.contrib import admin
from django.db import models
from player_tracking.models import Player, Transaction, AnnualRoster, MLBDraftDate, SummerLeague, SummerTeam


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    model = Player
    list_display = (
        "first",
        "last",
        "hsgrad_year",
        "bats",
        "throws",
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = (
        "player",
        "trans_event",
        "trans_date",
    )


@admin.register(AnnualRoster)
class AnnualRosterAdmin(admin.ModelAdmin):
    model = AnnualRoster
    list_display = (
        "spring_year",
        "team",
        "player",
        "status",
    )


@admin.register(MLBDraftDate)
class MLBDraftDateAdmin(admin.ModelAdmin):
    model = MLBDraftDate
    list_display = (
        "fall_year",
        "latest_birthdate",
        "latest_draft_day",
        "signing_deadline",
    )


@admin.register(SummerLeague)
class SummerLeagueAdmin(admin.ModelAdmin):
    model = SummerLeague
    list_display = (
        "league",
    )


@admin.register(SummerTeam)
class SummerTeamAdmin(admin.ModelAdmin):
    model = SummerTeam
    list_display = (
        "name",
        "mascot",
    )