from django.shortcuts import render
from django.db.models.functions import Lower

from index.views import save_traffic_data
from player_tracking.models import AnnualRoster
from player_tracking import choices
from player_tracking.views.player_locations import (
    calculate_outside_indiana_percentage,
)


def spring_depth_chart(request, spring_year):
    positions = [position[0] for position in choices.POSITIONS]
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
        "outside_indiana_percentage": calculate_outside_indiana_percentage(
            roster.player for roster in players
        ),
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/depth_chart.html", context)
