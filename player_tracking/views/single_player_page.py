from django.shortcuts import render, redirect
from django.db.models.functions import Lower
from django import http

from datetime import date

from player_tracking.models import (
    Player,
    Transaction,
    AnnualRoster,
    SummerAssign,
    Accolade,
)
from index.views import save_traffic_data


def view(request, player_id):
    try:
        player = Player.objects.get(pk=player_id)
    except Player.DoesNotExist:
        raise http.Http404
    rosters = AnnualRoster.objects.filter(player=player).order_by("-spring_year")
    transactions = Transaction.objects.filter(player=player).order_by("-trans_date")
    summers = SummerAssign.objects.filter(player=player).order_by("-summer_year")
    accolades = Accolade.objects.filter(player=player).order_by("-award_date")
    context = {
        "player": player,
        "page_title": f"{player.first} {player.last}",
        "rosters": rosters,
        "transactions": transactions,
        "summers": summers,
        "accolades": accolades,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/single_player_page.html", context)