from django.shortcuts import render, redirect
from django.contrib.auth import decorators
from django.urls import reverse

from player_tracking.models import Player
from player_tracking import forms


@decorators.login_required
def view(request, player_id):
    edit_info = Player.objects.get(pk=player_id)
    if request.method == "POST":
        form = forms.PlayerForm(request.POST)
        if form.is_valid():
            edit_info.first = form.cleaned_data["first"]
            edit_info.last = form.cleaned_data["last"]
            edit_info.hsgrad_year = form.cleaned_data["hsgrad_year"]
            edit_info.high_school = form.cleaned_data["high_school"]
            edit_info.home_city = form.cleaned_data["home_city"]
            edit_info.home_state = form.cleaned_data["home_state"]
            edit_info.home_country = form.cleaned_data["home_country"]
            edit_info.headshot = form.cleaned_data["headshot"]
            edit_info.action_shot = form.cleaned_data["action_shot"]
            edit_info.birthdate = form.cleaned_data["birthdate"]
            edit_info.bats = form.cleaned_data["bats"]
            edit_info.throws = form.cleaned_data["throws"]
            edit_info.height = form.cleaned_data["height"]
            edit_info.weight = form.cleaned_data["weight"]
            edit_info.primary_position = form.cleaned_data["primary_position"]
            edit_info.save()
        return redirect(reverse("single_player_page", args=[player_id]))
    else:
        form = forms.PlayerForm(
            initial={
                "first": edit_info.first,
                "last": edit_info.last,
                "hsgrad_year": edit_info.hsgrad_year,
                "high_school": edit_info.high_school,
                "home_city": edit_info.home_city,
                "home_state": edit_info.home_state,
                "home_country": edit_info.home_country,
                "headshot": edit_info.headshot,
                "action_shot": edit_info.action_shot,
                "birthdate": edit_info.birthdate,
                "bats": edit_info.bats,
                "throws": edit_info.throws,
                "height": edit_info.height,
                "weight": edit_info.weight,
                "primary_position": edit_info.primary_position,
            },
        )
        context = {
            "form": form,
            "player_id": player_id,
        }
        return render(request, "player_tracking/partials/edit_player.html", context)
