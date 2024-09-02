from django.shortcuts import render, redirect
from django.db.models.functions import Lower

from datetime import date

from player_tracking.models import (
    Player,
    Transaction,
    AnnualRoster,
    MLBDraftDate,
    SummerAssign,
)
from index.views import save_traffic_data
from player_tracking.choices import POSITION_CHOICES, ALL_ROSTER


def players(request):
    players = Player.objects.all().order_by(Lower("last"))
    context = {
        "players": players,
        "page_title": "Players",
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/players.html", context)


def pt_index(request):
    current_spring = date.today().year
    current_fall = current_spring - 1
    context = {
        "fall": current_fall,
        "spring": current_spring,
        "page_title": "Player Tracking",
        "this_year": str(date.today().year),
        "last_year": str(date.today().year - 1),
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/pt_index.html", context)
