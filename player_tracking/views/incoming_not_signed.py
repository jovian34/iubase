from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower

from player_tracking.models import Player, Transaction


@login_required
def view(request, fall_year):
    players = Player.objects.filter(first_spring=int(fall_year)+1).order_by(Lower("last"))
    for player in players:
        player.nli = False
        transactions = Transaction.objects.filter(player=player)
        for transaction in transactions:
            if transaction.trans_event == "National Letter of Intent Signed":
                player.nli = True
    context = {
        "players": players,
        "page_title": f"Commits for {fall_year} who have not yet signed a National Letter of Intent",
    }
    return render(request, "player_tracking/incoming_not_signed.html", context)