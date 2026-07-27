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
            "player__headshot",
        )
        .annotate(award_count=Count("id"))
        .order_by("-award_count", "player__last", "player__first")
    )


def group_leaders_by_award_count(leaders):
    award_groups = []
    for leader in leaders:
        if not award_groups or award_groups[-1]["award_count"] != leader["award_count"]:
            award_groups.append(
                {
                    "award_count": leader["award_count"],
                    "leaders": [],
                    "is_top_group": not award_groups,
                }
            )
        award_groups[-1]["leaders"].append(leader)
    return award_groups


def red_belt_award(title, leaders, description):
    return {
        "title": title,
        "groups": group_leaders_by_award_count(leaders),
        "description": description,
    }


def view(request, spring_year):
    denato_leaders = list(weekly_award_leaderboard("Joey DeNato", spring_year))
    denato_describe = "Named for the all-time Hoosier pitching wins leader (37 from 2011-2014)"
    dickerson_leaders = list(weekly_award_leaderboard("Alex Dickerson", spring_year))
    dickerson_describe = "Named for the prolific Hoosier slugger (2009-2011)"
    butler_leaders = list(weekly_award_leaderboard("Tony Butler", spring_year))
    butler_describe = "Named for the only Hoosier member of a Rawlings Gold Glove Team (2016 - 2B - 0 errors)"
    context = {
        "page_title": f"Red Belt Leaderboard for {spring_year}",
        "spring_year": spring_year,
        "denato_leaders": denato_leaders,
        "dickerson_leaders": dickerson_leaders,
        "butler_leaders": butler_leaders,
        "red_belt_awards": [
            red_belt_award("Joey DeNato Pitching Red Belts", denato_leaders, denato_describe),
            red_belt_award("Alex Dickerson Hitting Red Belts", dickerson_leaders, dickerson_describe),
            red_belt_award("Tony Butler Defense Red Belts", butler_leaders, butler_describe),
        ],
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/red_belt_leaderboard.html", context)
