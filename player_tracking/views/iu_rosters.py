from django.shortcuts import render, redirect

from datetime import date

from player_tracking.models import AnnualRoster
from player_tracking import choices
from index.views import save_traffic_data


def fall(request, fall_year):
    if request.META.get('HTTP_HX_REQUEST'):
        spring_year = int(fall_year) + 1
        players = (
            AnnualRoster.objects.filter(spring_year=spring_year)
            .filter(team__team_name="Indiana")
            .order_by("jersey")
        )
        years = [ int(fall_year) - 2 + i for i in range(5) ]
        context = {
            "fall_year": fall_year,
            "years": years,
            "players": players,
            "page_title": f"Fall {fall_year} Roster",
            "total": len(players),
        }
        return render(request, "player_tracking/partials/roster.html", context)
    else:
        return redirect("fall_players", fall_year=fall_year)


def spring(request, spring_year):
    players = (
        AnnualRoster.objects.filter(spring_year=spring_year)
        .filter(team__team_name="Indiana")
        .filter(status__in=choices.ALL_ROSTER)
        .order_by("jersey")
    )
    if len(players) < 5 and int(spring_year) >= date.today().year:
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