from django.shortcuts import render, redirect
from django.db.models.functions import Lower

from player_tracking.models import Player


def view(request, fall_year):
    if request.META.get('HTTP_HX_REQUEST'):
        spring_year = int(fall_year) + 1
        players = (
            Player.objects.filter(first_spring__lte=spring_year)
            .filter(last_spring__gte=spring_year)
            .order_by(Lower("last"))
        )
        years = [ int(fall_year) - 2 + i for i in range(5) ]
        context = {
            "fall_year": fall_year,
            "years": years,
            "players": players,
            "page_title": f"All Eligible Players For Fall {fall_year}",
            "count": len(players),
        }
        return render(request, "player_tracking/partials/all_eligible_players_fall.html", context)
    else:
        return redirect("fall_players", fall_year=fall_year)