from django.shortcuts import render
from django.db.models import Q

from player_tracking import models as pt_models
from index.views import save_traffic_data


def view(request, spring_year):
    players = pt_models.Player.objects.filter(
        Q(last_spring=spring_year) & Q(via_exhaust=True)
    )
    context = {
        "spring_year": spring_year,
        "players": players,
        "page_title": f"All players exhausting eligibility with Spring {spring_year}",
        "count": len(players),
    }
    save_traffic_data(request=request, page=context["page_title"])
    template_path = "player_tracking/exhausted_players.html"
    return render(request, template_path, context)
