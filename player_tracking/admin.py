from django.contrib import admin
from player_tracking import models


@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    model = models.Player
    list_display = (
        "first",
        "last",
        "hsgrad_year",
        "bats",
        "throws",
    )


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    model = models.Transaction
    list_display = (
        "player",
        "trans_event",
        "trans_date",
    )


@admin.register(models.AnnualRoster)
class AnnualRosterAdmin(admin.ModelAdmin):
    model = models.AnnualRoster
    list_display = (
        "spring_year",
        "team",
        "player",
        "status",
    )


@admin.register(models.MLBDraftDate)
class MLBDraftDateAdmin(admin.ModelAdmin):
    model = models.MLBDraftDate
    list_display = (
        "fall_year",
        "latest_birthdate",
        "latest_draft_day",
        "signing_deadline",
    )


@admin.register(models.SummerLeague)
class SummerLeagueAdmin(admin.ModelAdmin):
    model = models.SummerLeague
    list_display = ("league",)


@admin.register(models.ProfOrg)
class ProfOrgAdmin(admin.ModelAdmin):
    model = models.ProfOrg
    list_display = (
        "city",
        "mascot",
    )


@admin.register(models.SummerTeam)
class SummerTeamAdmin(admin.ModelAdmin):
    model = models.SummerTeam
    list_display = (
        "name",
        "mascot",
    )


@admin.register(models.SummerAssign)
class SummerAssignAdmin(admin.ModelAdmin):
    model = models.SummerAssign
    list_display = (
        "player",
        "summer_year",
        "summer_league",
        "summer_team",
    )


@admin.register(models.Accolade)
class AccoladeAdmin(admin.ModelAdmin):
    model = models.Accolade
    list_display = (
        "player",
        "award_date",
        "award_org",
        "name",
    )
