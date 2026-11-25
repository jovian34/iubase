from datetime import date

from django.shortcuts import render

from index.views import save_traffic_data
from player_tracking import choices
from player_tracking import models as pt_models


def view(request):
    today = date.today()
    this_year = today.year
    season_year = this_year + (1 if today.month in [11, 12] else 0)
    spring_roster_exists = pt_models.AnnualRoster.objects.filter(
        spring_year=season_year,
        team__team_name="Indiana",
        status__in=choices.ALL_ROSTER,
    ).exists()
    context = {
        "page_title": "Player Tracking",
        "this_year": str(this_year),
        "last_year": str(this_year - 1),
        "season_year": str(season_year),
        "previous_fall_year": str(season_year - 1),
        "spring_roster_exists": spring_roster_exists,
    }
    save_traffic_data(request=request, page=context["page_title"])
    template = (
        "player_tracking/pt_index_jul_oct.html"
        if 7 <= today.month <= 10
        else "player_tracking/pt_index_nov_jun.html"
    )
    return render(request, template, context)
