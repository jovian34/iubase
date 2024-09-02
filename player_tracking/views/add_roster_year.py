from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from datetime import date

from player_tracking.forms import AnnualRosterForm
from player_tracking.views.set_player_properties import set_player_props_get_errors
from player_tracking.models import AnnualRoster, Player, Team

@login_required
def view(request, player_id):
    if request.method == "POST":
        form = AnnualRosterForm(request.POST)
        if form.is_valid():
            save_roster_year(player_id, form)
            set_player_props_get_errors()
        return redirect(reverse("single_player_page", args=[player_id]))
    else:
        form = AnnualRosterForm(
            initial={
                "spring_year": date.today().year,
                "team": Team.objects.get(team_name="Indiana"),
            },
        )
        context = {
            "form": form,
            "player_id": player_id,
        }
        return render(
            request,
            "player_tracking/partials/add_roster_year.html",
            context,
        )


def save_roster_year(player_id, form):
    add_roster = AnnualRoster.objects.create(
        spring_year=form.cleaned_data["spring_year"],
        team=form.cleaned_data["team"],
        player=Player.objects.get(pk=player_id),
        jersey=form.cleaned_data["jersey"],
        status=form.cleaned_data["status"],
        primary_position=form.cleaned_data["primary_position"],
        secondary_position=form.cleaned_data["secondary_position"],
    )
    add_roster.save()