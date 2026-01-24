from django.shortcuts import render
from django.db.models import Q

from player_tracking.models import Player, Transaction
from index.views import save_traffic_data


def view(request, draft_year):
    players, count = set_drafted_player_info(int(draft_year))
    context = {
        "this_year": draft_year,
        "players": players,
        "page_title": f"All players selected in the {draft_year} MLB Draft",
        "count": count,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/drafted_players.html", context)


def draft_transactions(request):
    context = {
        "page_title": "All MLB Draft and Pro Signing Transactions",
        "transactions": Transaction.objects.filter(
            Q(trans_event="Signed Professional Contract")
            | Q(trans_event="Signed Professional Contract - Undrafted")
            | Q(trans_event="Drafted")
        ).order_by("-trans_date"),
    }
    return render(request, "player_tracking/draft_transactions.html", context)


def set_drafted_player_info(draft_year):
    players = Player.objects.filter(
        Q(hsgrad_year__lte=draft_year),
        Q(last_spring__isnull=True) | Q(last_spring__gte=draft_year),
    )
    count = 0
    for player in players:
        player.drafted = False
        player.signed = "no"
        transactions = Transaction.objects.filter(player=player).order_by("trans_date")
        for trans in transactions:
            if trans.trans_event == "Drafted" and trans.trans_date.year == draft_year:
                set_drafted_player(draft_year, player, trans)
                count += 1
            if (
                trans.trans_event == "Signed Professional Contract"
                and player.drafted
                and trans.trans_date.year == draft_year
            ):
                set_signed_player(player, trans)
            if (
                trans.trans_event == "Not Signing Professional Contract"
                and player.drafted
                and trans.trans_date.year == draft_year
            ):
                set_not_signed_player(player, trans)
    return players, count


def set_drafted_player(draft_year, player, trans):
    player.drafted = True
    player.position = trans.primary_position
    player.draft_round = trans.draft_round
    player.prof_org = trans.prof_org.__str__()
    player.slot = trans.bonus_or_slot
    player.draft_comment = trans.comment
    group_drafted_player(draft_year, player)


def group_drafted_player(draft_year, player):
    if player.hsgrad_year == draft_year:
        player.group = "High School Signee"
    else:
        player.group = "IU Player/Alumni"


def set_signed_player(player, trans):
    player.signed = "yes"
    player.bonus = trans.bonus_or_slot
    player.sign_comment = trans.comment
    player.bonus_pct = 100 * player.bonus / player.slot


def set_not_signed_player(player, trans):
    player.signed = "refused"
    player.sign_comment = trans.comment
