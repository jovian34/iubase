from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from datetime import date

from player_tracking.models import (
    Player,
    Transaction,
    AnnualRoster,
    MLBDraftDate,
    SummerAssign,
)
from live_game_blog.models import Team
from index.views import save_traffic_data
from player_tracking.forms import AnnualRosterForm, NewPlayerForm, TransactionForm, SummerAssignForm
from player_tracking.choices import (
    POSITION_CHOICES,
    LEFT,
    AFTER,
    GREY_SHIRT,
    RED_SHIRT,
    RED_SHIRT_PLUS_WAIVER,
)


def players(request):
    players = Player.objects.all().order_by("last")
    context = {
        "players": players,
        "page_title": "Players",
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/players.html", context)


def pt_index(request):
    today = timezone.now().date()
    if today.month < 8:
        current_spring = today.year
        current_fall = current_spring - 1
    else:
        current_fall = today.year
        current_spring = current_fall + 1
    context = {
        "fall": current_fall,
        "spring": current_spring,
        "page_title": "Player Tracking",
        "this_year": str(today.year),
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/pt_index.html", context)


def player_rosters(request, player_id):
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
    return render(request, "player_tracking/player_rosters.html", context)


def fall_depth_chart(request, fall_year):
    spring_year = int(fall_year) + 1
    fall_statuses = ["Fall Roster", "Spring Roster"]
    positions = [position[0] for position in POSITION_CHOICES]
    players = (
        AnnualRoster.objects.filter(spring_year=spring_year)
        .filter(team__team_name="Indiana")
        .filter(status__in=fall_statuses)
        .order_by("player__last")
    )
    context = {
        "players": players,
        "page_title": f"Fall {fall_year} Available Depth Chart",
        "positions": positions,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/depth_chart.html", context)


def spring_depth_chart(request, spring_year):
    positions = [position[0] for position in POSITION_CHOICES]
    players = (
        AnnualRoster.objects.filter(spring_year=spring_year)
        .filter(team__team_name="Indiana")
        .filter(status="Spring Roster")
        .order_by("player__last")
    )
    if players:
        page_title = f"Spring {spring_year} Available Depth Chart"
    else:
        page_title = f"Spring {spring_year} Roster not yet announced"
    context = {
        "players": players,
        "page_title": page_title,
        "positions": positions,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/depth_chart.html", context)


def fall_roster(request, fall_year):
    spring_year = int(fall_year) + 1
    players = (
        AnnualRoster.objects.filter(spring_year=spring_year)
        .filter(team__team_name="Indiana")
        .order_by("jersey")
    )
    context = {
        "players": players,
        "page_title": f"Fall {fall_year} Roster",
        "total": len(players),
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/roster.html", context)


def spring_roster(request, spring_year):
    all_roster = [
        "Spring Roster",
        "On Spring Roster but did not play",
        "Played but granted eligibility waiver",
    ]
    players = (
        AnnualRoster.objects.filter(spring_year=spring_year)
        .filter(team__team_name="Indiana")
        .filter(status__in=all_roster)
        .order_by("jersey")
    )
    if len(players) < 5 and int(spring_year) >= timezone.now().date().year:
        page_title = f"Spring {spring_year} Roster not fully announced"
    else:
        page_title = f"Spring {spring_year} Roster"
    context = {
        "players": players,
        "page_title": page_title,
        "total": len(players),
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/roster.html", context)


def portal(request, portal_year):
    outgoing = Transaction.objects.filter(
        trans_event="Entered Transfer Portal",
        trans_date__year=portal_year,
    ).order_by("player__last")
    incoming = Transaction.objects.filter(
        trans_event="Verbal Commitment from College",
        trans_date__year=portal_year,
    ).order_by("player__last")
    context = {
        "outgoing": outgoing,
        "incoming": incoming,
        "page_title": f"{portal_year} Transfer Portal",
        "total_out": str(len(outgoing)),
        "total_in": str(len(incoming)),
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/portal.html", context)


def sort_by_positions(players):
    lhp = {"position": "Left Handed Pitcher", "players": [],}
    rhp = {"position": "Right Handed Pitcher", "players": [],}
    catcher = {"position": "Catcher", "players": [],}
    infielder = {"position": "Infielder", "players": [],}
    outfielder = {"position": "Outfielder", "players": [],}
    dh = {"position": "Designated Hitter", "players": [],}
    for player in players:
        if player.throws == "Left" and player.position == "Pitcher":
            lhp["players"].append(player)
        elif player.throws == "Right" and player.position == "Pitcher":
            rhp["players"].append(player)
        elif player.position == "Catcher":
            catcher["players"].append(player)
        elif player.position in ["First Base", "Second Base", "Third Base", "Shortstop"]:
            infielder["players"].append(player)
        elif player.position in ["Centerfield", "Corner Outfield"]:
            outfielder["players"].append(player)
        else:
            dh["players"].append(player)
    positions = [lhp, rhp, catcher, infielder, outfielder, dh]
    for position in positions:
        position["count"] = len(position["players"])
    return positions


def projected_players_fall(request, fall_year):
    try:
        draft_date = MLBDraftDate.objects.get(fall_year=fall_year)
    except MLBDraftDate.DoesNotExist:
        return redirect("pt_index")
    
    if int(fall_year) < date.today().year:
        return redirect("pt_index")
    
    players = Player.objects.filter(last_spring__gte=(int(fall_year) + 1)).order_by(
        "last"
    )

    draft_pending = True
    if draft_date.latest_draft_day < date.today():
        draft_pending = False
    if draft_date.draft_complete:
        draft_pending = False
    for player in players:
        roster_draft = AnnualRoster.objects.filter(player=player)
        if len(roster_draft) > 2 and draft_pending:
            player.draft = f"*{fall_year} MLB Draft Eligible"
        roster = AnnualRoster.objects.filter(
            player=player, spring_year=fall_year
        ).first()
        if roster:
            if player.birthdate:
                if player.birthdate <= draft_date.latest_birthdate and draft_pending:
                    player.draft = f"*{fall_year} MLB Draft Eligible"
            player.position = roster.primary_position
            if roster.team.mascot == "Hoosiers":
                player.group = "Returning"
            else:
                player.group = "Transfer"
        else:
            player.group = "Freshman"
            if draft_pending:
                player.draft = f"*{fall_year} MLB Draft Eligible from High School"
            sep1 = date(int(fall_year), 9, 1)
            transactions = Transaction.objects.filter(
                player=player, trans_date__lte=sep1
            ).order_by("-trans_date")
            for transaction in transactions:
                if transaction.primary_position:
                    player.position = transaction.primary_position
                    break
                else:
                    player.position = None
    count = len(players)
    positions = sort_by_positions(players)
    context = {
        "players": players,
        "page_title": f"Projected Players For Fall {fall_year}",
        "count": count,
        "positions": positions,    
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/projected_players_fall.html", context)


def draft_combine_attendees(request, this_year):
    draft_date = MLBDraftDate.objects.get(fall_year=int(this_year))
    draft_date = draft_date.latest_draft_day

    count = 0
    players = Player.objects.all().order_by("last")
    for player in players:
        player.combine = False
        transactions = Transaction.objects.filter(player=player)
        for trans in transactions:
            if trans.trans_event == "Attending MLB Draft Combine" and trans.trans_date.year == int(this_year):
                player.combine = True
                player.position = trans.primary_position
                count += 1     
                if player.hsgrad_year == int(this_year):
                    player.group = "Freshman"
                else:
                    player.group = "College"

    context = {
        "this_year": this_year,
        "players": players,
        "page_title": f"All players in the {this_year} MLB Draft Combine",
        "count": count,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/draft_combine_attendees.html", context)


def summer_assignments(request, summer_year):
    assignments = SummerAssign.objects.filter(summer_year=summer_year).order_by("player__last")
    context = {
        "page_title": f"{summer_year} College Summer League Assignments for current and former Indiana players",
        "assignments": assignments,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/summer_assignments.html", context)


def drafted_players(request, draft_year):
    count = 0
    players = Player.objects.all().order_by("last")
    for player in players:
        player.drafted = False
        player.signed = False
        transactions = Transaction.objects.filter(player=player).order_by("trans_date")
        for trans in transactions:
            if trans.trans_event == "Drafted" and trans.trans_date.year == int(draft_year):
                player.drafted = True
                player.position = trans.primary_position
                player.draft_round = trans.draft_round
                player.prof_org = trans.prof_org.__str__()
                player.slot = trans.bonus_or_slot
                player.draft_comment = trans.comment
                count += 1     
                if player.hsgrad_year == int(draft_year):
                    player.group = "High School Signee"
                else:
                    player.group = "IU Player/Alumni"
            if trans.trans_event == "Signed Professional Contract" and player.drafted and trans.trans_date.year == int(draft_year):
                player.signed = True
                player.bonus = trans.bonus_or_slot
                player.sign_comment = trans.comment
                player.bonus_pct = 100 * player.bonus / player.slot
    context = {
        "this_year": draft_year,
        "players": players,
        "page_title": f"All players selected in the {draft_year} MLB Draft",
        "count": count,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/drafted_players.html", context)