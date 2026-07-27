from django.db.models import Count
from django.shortcuts import render

from index.views import save_traffic_data
from player_tracking import models as pt_models


def weekly_award_leaderboard(award_phrase, spring_year):
    return (
        pt_models.Accolade.objects.filter(
            name__icontains="weekly",
            award_date__year=spring_year,
        )
        .filter(name__icontains=award_phrase)
        .values(
            "player__id",
            "player__first",
            "player__last",
        )
        .annotate(award_count=Count("id"))
        .order_by("-award_count", "player__last", "player__first")
    )


def view(request, spring_year):
    context = {
        "page_title": f"Red Belt Leaderboard for {spring_year}",
        "spring_year": spring_year,
        "denato_leaders": weekly_award_leaderboard("Joey DeNato", spring_year),
        "dickerson_leaders": weekly_award_leaderboard("Alex Dickerson", spring_year),
        "butler_leaders": weekly_award_leaderboard("Tony Butler", spring_year),
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/red_belt_leaderboard.html", context)
