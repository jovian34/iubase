from django.db.models.functions import Lower

from datetime import date

from player_tracking.models import (
    Player,
    Transaction,
    AnnualRoster,
    MLBDraftDate,
)


def sort_by_positions(players):
    lhp = {
        "position": "Left Handed Pitcher",
        "players": [],
    }
    rhp = {
        "position": "Right Handed Pitcher",
        "players": [],
    }
    catcher = {
        "position": "Catcher",
        "players": [],
    }
    infielder = {
        "position": "Infielder",
        "players": [],
    }
    outfielder = {
        "position": "Outfielder",
        "players": [],
    }
    dh = {
        "position": "Designated Hitter",
        "players": [],
    }
    for player in players:
        if player.throws == "Left" and player.position == "Pitcher":
            lhp["players"].append(player)
        elif player.throws == "Right" and player.position == "Pitcher":
            rhp["players"].append(player)
        elif player.position == "Catcher":
            catcher["players"].append(player)
        elif player.position in [
            "First Base",
            "Second Base",
            "Third Base",
            "Shortstop",
        ]:
            infielder["players"].append(player)
        elif player.position in ["Centerfield", "Corner Outfield"]:
            outfielder["players"].append(player)
        else:
            dh["players"].append(player)
    positions = [lhp, rhp, catcher, infielder, outfielder, dh]
    for position in positions:
        position["count"] = len(position["players"])
    return positions


def is_draft_pending(draft_date):
    draft_pending = True
    if draft_date.latest_draft_day < date.today():
        draft_pending = False
    if draft_date.draft_complete:
        draft_pending = False
    return draft_pending


def set_roster_player(fall_year, draft_date, draft_pending, player, roster):
    if player.birthdate:
        if player.birthdate <= draft_date.latest_birthdate and draft_pending:
            player.draft = f"*{fall_year} MLB Draft Eligible"
    player.position = roster.primary_position
    if roster.team.mascot == "Hoosiers":
        player.group = "Returning"
    else:
        player.group = "Transfer"


def set_freshman(fall_year, draft_pending, player):
    player.group = "Freshman"
    if draft_pending:
        player.draft = f"*{fall_year} MLB Draft Eligible from High School"
    transactions = Transaction.objects.filter(
        player=player, trans_date__lte=date(int(fall_year), 9, 1)
    ).order_by("-trans_date")
    for transaction in transactions:
        if transaction.primary_position:
            player.position = transaction.primary_position
            break
        else:
            player.position = None


def set_player_info(fall_year, draft_date, draft_pending, players):
    for player in players:
        player.draft = None
        roster_draft = AnnualRoster.objects.filter(player=player)
        if len(roster_draft) > 2 and draft_pending:
            player.draft = f"*{fall_year} MLB Draft Eligible"
        roster = AnnualRoster.objects.filter(
            player=player, spring_year=fall_year
        ).first()
        if roster:
            set_roster_player(fall_year, draft_date, draft_pending, player, roster)
        else:
            set_freshman(fall_year, draft_pending, player)


def set_fall_player_projection_info(fall_year):
    draft_date = MLBDraftDate.objects.get(fall_year=fall_year)
    players = (
        Player.objects.filter(first_spring__lte=(int(fall_year) + 1))
        .filter(last_spring__gte=(int(fall_year) + 1))
        .order_by(Lower("last"))
    )
    draft_pending = is_draft_pending(draft_date)
    set_player_info(fall_year, draft_date, draft_pending, players)
    return players
