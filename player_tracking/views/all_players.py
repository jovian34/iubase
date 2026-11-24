from django.db.models.functions import Lower
from django.shortcuts import render

from index.views import save_traffic_data
from player_tracking.models import Player


def view(request):
    players = Player.objects.all().order_by(Lower("last"))
    context = {
        "players": players,
        "page_title": "Players",
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/players.html", context)
