from django import shortcuts
from django.contrib.auth import decorators
from django import urls

import datetime

from player_tracking import forms as pt_forms
from player_tracking.views import set_player_properties
from player_tracking import models as pt_models
from live_game_blog import models as lgb_models

@decorators.login_required
def view(request, player_id):
    if request.method == "POST":
        form = pt_forms.AnnualRosterForm(request.POST)
        if form.is_valid():
            save_roster_year(player_id, form)
            set_player_properties.set_player_props_get_errors()
        return shortcuts.redirect(urls.reverse("single_player_page", args=[player_id]))
    else:
        form = pt_forms.AnnualRosterForm(
            initial={
                "spring_year": datetime.date.today().year,
                "team": lgb_models.Team.objects.get(team_name="Indiana"),
            },
        )
        context = {
            "form": form,
            "player_id": player_id,
        }
        return shortcuts.render(
            request,
            "player_tracking/partials/add_roster_year.html",
            context,
        )


def save_roster_year(player_id, form):
    add_roster = pt_models.AnnualRoster.objects.create(
        spring_year=form.cleaned_data["spring_year"],
        team=form.cleaned_data["team"],
        player=pt_models.Player.objects.get(pk=player_id),
        jersey=form.cleaned_data["jersey"],
        status=form.cleaned_data["status"],
        primary_position=form.cleaned_data["primary_position"],
        secondary_position=form.cleaned_data["secondary_position"],
    )
    add_roster.save()