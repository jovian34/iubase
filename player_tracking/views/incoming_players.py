from django.shortcuts import render
from django.db.models.functions import Lower

from player_tracking.models import Player, Transaction
from index.views import save_traffic_data


def calculate_outside_indiana_percentage(players):
    players_with_state = players.filter(home_state__isnull=False).exclude(home_state="")
    player_count = players_with_state.count()
    if player_count == 0:
        return 0
    outside_indiana_count = players_with_state.exclude(home_state="IN").count()
    return round(outside_indiana_count / player_count * 100)


def view(request, fall_year):
    players = Player.objects.filter(first_spring=int(fall_year) + 1).order_by(
        Lower("last")
    )
    for player in players:
        if int(fall_year) == player.hsgrad_year:
            player.hs = True
        else:
            player.hs = False
        player.nli = False
        transactions = Transaction.objects.filter(player=player)
        nli = "National Letter of Intent Signed"
        for transaction in transactions:
            age_of_nli = int(fall_year) - transaction.trans_date.year
            if transaction.trans_event == nli and age_of_nli < 2:
                player.nli = True
    context = {
        "players": players,
        "page_title": f"Incoming players for Fall {int(fall_year)}",
        "outside_indiana_percentage": calculate_outside_indiana_percentage(players),
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/incoming_players.html", context)
