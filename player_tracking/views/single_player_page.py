from django.shortcuts import render, redirect
from django.db.models.functions import Lower

from datetime import date

from player_tracking.models import (
    Player,
    Transaction,
    AnnualRoster,
    SummerAssign,
)
from index.views import save_traffic_data


def view(request, player_id):
    player = Player.objects.get(pk=player_id)
    rosters = AnnualRoster.objects.filter(player=player).order_by("-spring_year")
    transactions = Transaction.objects.filter(player=player).order_by("-trans_date")
    summers = SummerAssign.objects.filter(player=player).order_by("-summer_year")
    context = {
        "player": player,
        "page_title": f"{player.first} {player.last}",
        "rosters": rosters,
        "transactions": transactions,
        "summers": summers,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/single_player_page.html", context)