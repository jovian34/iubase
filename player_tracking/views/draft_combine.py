from django.shortcuts import render

from player_tracking.models import Player, Transaction
from index.views import save_traffic_data


def view(request, draft_year):
    count, players = set_combine_attendee_count_and_info(draft_year)
    context = {
        "players": players,
        "page_title": f"All players in the {draft_year} MLB Draft Combine",
        "count": count,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/draft_combine.html", context)


def set_combine_attendee_count_and_info(draft_year):
    count = 0
    players = Player.objects.all().order_by("last")
    for player in players:
        player.combine = False
        transactions = Transaction.objects.filter(player=player)
        for trans in transactions:
            if (
                trans.trans_event == "Attending MLB Draft Combine"
                and trans.trans_date.year == int(draft_year)
            ):
                count += 1
                set_draft_combine_player_props(draft_year, player, trans)
    return count, players


def set_draft_combine_player_props(draft_year, player, trans):
    player.combine = True
    player.position = trans.primary_position
    if player.hsgrad_year == int(draft_year):
        player.group = "Freshman"
    else:
        player.group = "College"
