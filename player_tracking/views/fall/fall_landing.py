from django.shortcuts import render, redirect

from datetime import date

from player_tracking.models import AnnualRoster, MLBDraftDate
from index.views import save_traffic_data


def view(request, fall_year=date.today().year):
    context = {
        "fall_year": fall_year,
        "page_title": "Players for Fall Seasons by Year",
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/fall_players.html", context)


def redirect_to_roster_projection_or_eligible(request, fall_year):
    spring_year = int(fall_year) + 1
    if AnnualRoster.objects.filter(spring_year=spring_year):
        return redirect("fall_roster", fall_year=fall_year)
    elif int(fall_year) == date.today().year and does_mlb_draft_date_exist_for_year(
        fall_year
    ):
        return redirect("projected_players_fall_depth", fall_year=fall_year)
    else:
        return redirect("all_eligible_players_fall", fall_year=fall_year)


def does_mlb_draft_date_exist_for_year(fall_year):
    try:
        MLBDraftDate.objects.get(fall_year=fall_year)
        return True
    except MLBDraftDate.DoesNotExist:
        return False
