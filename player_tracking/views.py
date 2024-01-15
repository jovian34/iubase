from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse

from player_tracking.models import Player, Transaction, AnnualRoster
from live_game_blog.models import Team
from player_tracking.forms import AnnualRosterForm


def players(request):
    players = Player.objects.all()
    context = {
        "players": players,
        "page_title": "Players",
    }
    return render(request, "player_tracking/players.html", context)


def player_rosters(request, player_id):
    player = Player.objects.get(pk=player_id)
    rosters = AnnualRoster.objects.filter(player=player).order_by("-spring_year")
    context = {
        "player": player,
        "page_title": f"{player.first} {player.last} rosters",
        "rosters": rosters,
    }
    return render(request, "player_tracking/player_rosters.html", context)



def add_roster_year(request, player_id):
    if request.method == "POST":
        print(request.POST)
        form = AnnualRosterForm(request.POST)
        if form.is_valid():
            add_roster = AnnualRoster.objects.create(
                spring_year=form.cleaned_data["spring_year"],
                team=form.cleaned_data["team"],
                player=Player.objects.get(pk=player_id),
                jersey=form.cleaned_data["jersey"],
                status=form.cleaned_data["status"],
                primary_position=form.cleaned_data["primary_position"],
                secondary_position=form.cleaned_data["secondary_position"]
            )
            add_roster.save()
        else:
            print("FORM IS NOT VALID")

        return redirect(reverse("player_rosters", args=[player_id]))
    else:
        player = Player.objects.get(pk=player_id)
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
            request, "player_tracking/partials/add_roster_year.html", context,
        )