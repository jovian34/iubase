from django.shortcuts import render

from player_tracking.models import Player, Transaction, AnnualRoster


def players(request):
    players = Player.objects.all()
    context = {
        "players": players,
        "page_title": "Players",
    }
    return render(request, "player_tracking/players.html", context)


def player_rosters(request, player_id):
    player = Player.objects.get(pk=player_id)
    rosters = AnnualRoster.objects.filter(player=player)
    context = {
        "player": player,
        "page_title": f"{player.first} {player.last} rosters",
        "rosters": rosters,
    }
    return render(request, "player_tracking/player_rosters.html", context)