from django.shortcuts import render
from django.db.models.functions import Lower

from index.views import save_traffic_data
from player_tracking.models import AnnualRoster
from player_tracking.choices import POSITION_CHOICES


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