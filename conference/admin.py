from django.contrib import admin

from conference import models as conf_models


@admin.register(conf_models.Conference)
class ConferenceAdmin(admin.ModelAdmin):
    model = conf_models.Conference
    list_display = (
        "abbrev",
        "long_name",
    )


@admin.register(conf_models.ConfTeam)
class ConfTeamAdmin(admin.ModelAdmin):
    model = conf_models.ConfTeam
    list_display = (
        "team",
        "conference",
        "fall_year_joined",
    )