from django import forms, http, shortcuts
from django.contrib.auth import decorators as auth
from django.db import transaction

from player_tracking import forms as pt_forms
from player_tracking import models as pt_models
from player_tracking.views.fall.fall_projection import set_fall_player_projection_info
from player_tracking.views import set_player_properties
from live_game_blog.models import Team


@auth.login_required
def view(request, fall_year):
    if not request.user.has_perm("player_tracking.add_annualroster"):
        return http.HttpResponseForbidden()

    projected_players = list(set_fall_player_projection_info(fall_year))
    spring_year = int(fall_year) + 1
    players = [
        player
        for player in projected_players
        if not pt_models.AnnualRoster.objects.filter(
            player=player, spring_year=spring_year
        ).exists()
    ]
    formset_class = forms.formset_factory(pt_forms.FallRosterEntryForm, extra=0)
    initial = [
        {"player": player.pk, "primary_position": player.position}
        for player in players
    ]
    formset = formset_class(request.POST or None, initial=initial)

    if request.method == "POST" and formset.is_valid():
        save_roster_entries(formset, projected_players, spring_year)
        set_player_properties.set_player_props_get_errors()

    context = {
        "fall_year": fall_year,
        "spring_year": spring_year,
        "formset": formset,
        "players": players,
        "player_forms": zip(players, formset.forms),
    }
    return shortcuts.render(
        request,
        "player_tracking/partials/enter_fall_roster.html",
        context,
    )


@transaction.atomic
def save_roster_entries(formset, players, spring_year):
    projected_players = {player.pk: player for player in players}
    team = Team.objects.get(team_name="Indiana")
    for form in formset:
        if not form.cleaned_data or form.cleaned_data.get("jersey") is None:
            continue
        player = projected_players[form.cleaned_data["player"]]
        if pt_models.AnnualRoster.objects.filter(
            player=player, spring_year=spring_year
        ).exists():
            continue
        pt_models.AnnualRoster.objects.create(
            spring_year=spring_year,
            team=team,
            player=player,
            jersey=form.cleaned_data["jersey"],
            status="Fall Roster",
            primary_position=form.cleaned_data["primary_position"],
        )
