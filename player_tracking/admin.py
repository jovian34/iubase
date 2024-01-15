from django.contrib import admin
from django.db import models
from player_tracking.models import Player, Transaction, AnnualRoster


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    model = Player
    list_display = (
        "first",
        "last",
        "hsgrad_year",
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
        "fall_year",
        "player",
        "status",
    )
