from django.shortcuts import render
from django.db.models.functions import Lower

from player_tracking.models import SummerAssign
from index.views import save_traffic_data


def view(request, summer_year):
    assignments = SummerAssign.objects.filter(summer_year=summer_year).order_by(
        Lower("player__last")
    )
    context = {
        "page_title": f"{summer_year} College Summer League Assignments for current and former Indiana players",
        "assignments": assignments,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/summer_assignments.html", context)