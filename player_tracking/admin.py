from django.contrib import admin
from django.db import models
from player_tracking.models import Player, Transaction, AnnualRoster, MLBDraftDate


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
class MLBDraftDate(admin.ModelAdmin):
    model = MLBDraftDate
    list_display = (
        "fall_year",
        "latest_birthdate",
        "latest_draft_day",
        "signing_deadline",
    )
