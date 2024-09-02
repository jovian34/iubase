from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from datetime import date

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
)
from player_tracking.views.set_player_properties import set_player_props_get_errors


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
                "hsgrad_year": date.today().year,
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


@login_required
def add_summer_assignment(request, player_id):
    if request.method == "POST":
        form = SummerAssignForm(request.POST)
        if form.is_valid():
            save_summer_assign(player_id, form)
        return redirect(reverse("single_player_page", args=[player_id]))
    else:
        form = SummerAssignForm(
            initial={
                "summer_year": date.today().year,
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
        return redirect(reverse("single_player_page", args=[player_id]))
    else:
        form = TransactionForm(
            initial={
                "trans_date": date.today(),
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
