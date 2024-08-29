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


def group_drafted_player(draft_year, player):
    if player.hsgrad_year == int(draft_year):
        player.group = "High School Signee"
    else:
        player.group = "IU Player/Alumni"


def set_draft_combine_player_props(draft_year, player, trans):
    player.combine = True
    player.position = trans.primary_position
    if player.hsgrad_year == int(draft_year):
        player.group = "Freshman"
    else:
        player.group = "College"


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


def set_drafted_player(draft_year, player, trans):
    player.drafted = True
    player.position = trans.primary_position
    player.draft_round = trans.draft_round
    player.prof_org = trans.prof_org.__str__()
    player.slot = trans.bonus_or_slot
    player.draft_comment = trans.comment
    group_drafted_player(draft_year, player)


def set_signed_player(player, trans):
    player.signed = "yes"
    player.bonus = trans.bonus_or_slot
    player.sign_comment = trans.comment
    player.bonus_pct = 100 * player.bonus / player.slot


def set_not_signed_player(player, trans):
    player.signed = "refused"
    player.sign_comment = trans.comment


def set_drafted_player_info(draft_year):
    players = Player.objects.all().order_by(Lower("last"))
    count = 0
    for player in players:
        player.drafted = False
        player.signed = "no"
        transactions = Transaction.objects.filter(player=player).order_by("trans_date")
        for trans in transactions:
            if trans.trans_event == "Drafted" and trans.trans_date.year == int(
                draft_year
            ):
                set_drafted_player(draft_year, player, trans)
                count += 1
            if (
                trans.trans_event == "Signed Professional Contract"
                and player.drafted
                and trans.trans_date.year == int(draft_year)
            ):
                set_signed_player(player, trans)
            if (
                trans.trans_event == "Not Signing Professional Contract"
                and player.drafted
                and trans.trans_date.year == int(draft_year)
            ):
                set_not_signed_player(player, trans)
    return players, count
