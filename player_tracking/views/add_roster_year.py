from django import shortcuts
from django.contrib.auth import decorators as auth
from django import http, urls

import datetime

from player_tracking import forms as pt_forms
from player_tracking.views import set_player_properties
from player_tracking import models as pt_models
from live_game_blog import models as lgb_models


@auth.login_required
def view(request, player_id):
    if not request.user.has_perm("player_tracking.add_annualroster"):
        return http.HttpResponseForbidden()
    elif request.method == "POST":
        return validate_post_annual_roster_form_save_then_redirect(request, player_id)
    else:
        context = {
            "form": initialize_annual_roster_form(),
            "player_id": player_id,
        }
        template_path = "player_tracking/partials/add_roster_year.html"
        return shortcuts.render(request, template_path, context)


def initialize_annual_roster_form():
    return pt_forms.AnnualRosterForm(
        initial={
            "spring_year": datetime.date.today().year,
            "team": lgb_models.Team.objects.get(team_name="Indiana"),
        },
    )


def validate_post_annual_roster_form_save_then_redirect(request, player_id):
    form = pt_forms.AnnualRosterForm(request.POST)
    if form.is_valid():
        save_roster_year(player_id, form)
        set_player_properties.set_player_props_get_errors()
    return shortcuts.redirect(urls.reverse("single_player_page", args=[player_id]))


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
