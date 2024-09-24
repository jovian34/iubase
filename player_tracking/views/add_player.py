from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from datetime import date

from player_tracking.models import Player, Transaction
from player_tracking.forms import NewPlayerForm
from player_tracking.views.set_player_properties import set_player_props_get_errors


@login_required
def view(request):
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


def save_new_player_and_init_transaction(form):
    add_player = Player.objects.create(
        first=form.cleaned_data["first"],
        last=form.cleaned_data["last"],
        hsgrad_year=form.cleaned_data["hsgrad_year"],
        high_school=form.cleaned_data["high_school"],
        home_city=form.cleaned_data["home_city"],
        home_state=form.cleaned_data["home_state"],
        home_country=form.cleaned_data["home_country"],
        headshot=form.cleaned_data["headshot"],
        birthdate=form.cleaned_data["birthdate"],
        bats=form.cleaned_data["bats"],
        throws=form.cleaned_data["throws"],
        height=form.cleaned_data["height"],
        weight=form.cleaned_data["weight"],
        primary_position=form.cleaned_data["primary_position"],
    )
    add_player.save()
    this_player = Player.objects.last()
    add_initial_transaction = Transaction(
        player=this_player,
        trans_event=form.cleaned_data["trans_event"],
        trans_date=form.cleaned_data["trans_date"],
        citation=form.cleaned_data["citation"],
        primary_position=form.cleaned_data["primary_position"],
    )
    add_initial_transaction.save()
