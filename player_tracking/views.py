from django.shortcuts import render

from player_tracking.models import Player, Transaction, AnnualRoster


def players(request):
    players = Player.objects.all()
    context = {
        "players": players,
        "page_title": "Players",
    }
    return render(request, "player_tracking/players.html", context)
