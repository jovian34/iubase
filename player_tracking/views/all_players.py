from django.shortcuts import render
from django.db.models.functions import Lower

from player_tracking.models import Player
from index.views import save_traffic_data


def view(request):
    players = Player.objects.all().order_by(Lower("last"))
    context = {
        "players": players,
        "page_title": "Players",
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/players.html", context)