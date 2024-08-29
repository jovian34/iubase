from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from player_tracking.models import Player
from live_game_blog.models import Team
from player_tracking.forms import (
    AnnualRosterForm,
    NewPlayerForm,
    TransactionForm,
    SummerAssignForm,
)
from player_tracking.views.changes_logic import (
    save_new_player_and_init_transaction,
    save_transaction_form,
    save_roster_year,
    save_summer_assign,
    set_player_props_get_errors,
)


@login_required
def add_player(request):
    if request.method == "POST":
        form = NewPlayerForm(request.POST)
        if form.is_valid():
            save_new_player_and_init_transaction(form)
            set_player_props_get_errors()
        return redirect(reverse("players"))
    else:
        form = NewPlayerForm(
            initial={
                "hsgrad_year": timezone.now().year,
                "home_country": "USA",
            },
        )
        context = {
            "form": form,
            "page_title": "Add a New Player",
        }
        return render(request, "player_tracking/add_player.html", context)


@login_required
def add_roster_year(request, player_id):
    if request.method == "POST":
        form = AnnualRosterForm(request.POST)
        if form.is_valid():
            save_roster_year(player_id, form)
            set_player_props_get_errors()
        return redirect(reverse("player_rosters", args=[player_id]))
    else:
        form = AnnualRosterForm(
            initial={
                "spring_year": timezone.now().year,
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


@login_required
def add_summer_assignment(request, player_id):
    if request.method == "POST":
        form = SummerAssignForm(request.POST)
        if form.is_valid():
            save_summer_assign(player_id, form)
        return redirect(reverse("player_rosters", args=[player_id]))
    else:
        form = SummerAssignForm(
            initial={
                "summer_year": timezone.now().year,
            },
        )
        context = {
            "player_id": player_id,
            "form": form,
        }
        return render(
            request,
            "player_tracking/partials/add_summer_assignment.html",
            context,
        )


@login_required
def add_transaction(request, player_id):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            save_transaction_form(player_id, form)
            set_player_props_get_errors()
        return redirect(reverse("player_rosters", args=[player_id]))
    else:
        form = TransactionForm(
            initial={
                "trans_date": timezone.now().year,
            },
        )
        context = {
            "form": form,
            "player_id": player_id,
        }
        return render(
            request,
            "player_tracking/partials/add_transaction.html",
            context,
        )


@login_required
def set_player_properties(request):
    errors = set_player_props_get_errors()
    players_updated = Player.objects.all().order_by("last")
    context = {
        "players": players_updated,
        "error_exists": bool(len(errors)),
        "errors": errors,
        "page_title": "Errors From Last Spring Calculations",
    }
    return render(request, "player_tracking/calc_last_spring.html", context)
