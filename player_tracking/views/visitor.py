from django.shortcuts import render, redirect
from django.utils import timezone
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
from player_tracking.views.visitor_logic import (
    set_draft_combine_player_props,
    sort_by_positions,
    set_fall_player_projection_info,
    set_drafted_player_info,
    set_combine_attendee_count_and_info
)


def players(request):
    players = Player.objects.all().order_by(Lower("last"))
    context = {
        "players": players,
        "page_title": "Players",
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/players.html", context)


def pt_index(request):
    if date.today().month < 9:
        current_spring = date.today().year
        current_fall = current_spring - 1
    else:
        current_fall = date.today().year
        current_spring = current_fall + 1
    context = {
        "fall": current_fall,
        "spring": current_spring,
        "page_title": "Player Tracking",
        "this_year": str(date.today().year),
        "last_year": str(date.today().year - 1),
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
        .order_by(Lower("player__last"))
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
        .order_by(Lower("player__last"))
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
    players = (
        AnnualRoster.objects.filter(spring_year=spring_year)
        .filter(team__team_name="Indiana")
        .filter(status__in=ALL_ROSTER)
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
    ).order_by(Lower("player__last"))
    context = {
        "outgoing": outgoing,
        "incoming": incoming,
        "page_title": f"{portal_year} Transfer Portal",
        "total_out": str(len(outgoing)),
        "total_in": str(len(incoming)),
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/portal.html", context)


def all_eligible_players_fall(request, fall_year):
    spring_year = int(fall_year) + 1
    players = Player.objects.filter(first_spring__lte=spring_year).filter(last_spring__gte=spring_year).order_by(Lower("last"))
    context = {
        "players": players,
        "page_title": f"All Eligible Players For Fall {fall_year}",
        "count": len(players),
    }
    return render(request, "player_tracking/all_eligible_players_fall.html", context)


def fall_players(request, fall_year):
    spring_year = int(fall_year) + 1
    if AnnualRoster.objects.filter(spring_year=spring_year):
        return redirect("fall_roster", fall_year=fall_year)
    elif int(fall_year) < date.today().year:
        return redirect("pt_index")
    elif int(fall_year) > date.today().year or not MLBDraftDate.objects.get(fall_year=fall_year):
        return redirect("all_eligible_players_fall", fall_year=fall_year)
    else:
        return redirect("projected_players_fall", fall_year=fall_year)


def projected_players_fall(request, fall_year):
    spring_year = int(fall_year) + 1
    if AnnualRoster.objects.filter(spring_year=spring_year):
        return redirect("fall_roster", fall_year=fall_year)
    elif int(fall_year) < date.today().year:
        return redirect("pt_index")
    elif int(fall_year) > date.today().year or not MLBDraftDate.objects.get(fall_year=fall_year):
        return redirect("all_eligible_players_fall", fall_year=fall_year)
        
    players = set_fall_player_projection_info(fall_year)
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


def draft_combine_attendees(request, draft_year):
    count, players = set_combine_attendee_count_and_info(draft_year)
    context = {
        "players": players,
        "page_title": f"All players in the {draft_year} MLB Draft Combine",
        "count": count,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/draft_combine_attendees.html", context)


def summer_assignments(request, summer_year):
    assignments = SummerAssign.objects.filter(summer_year=summer_year).order_by(Lower("player__last"))
    context = {
        "page_title": f"{summer_year} College Summer League Assignments for current and former Indiana players",
        "assignments": assignments,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/summer_assignments.html", context)


def drafted_players(request, draft_year):
    players, count = set_drafted_player_info(draft_year)
    context = {
        "this_year": draft_year,
        "players": players,
        "page_title": f"All players selected in the {draft_year} MLB Draft",
        "count": count,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/drafted_players.html", context)





