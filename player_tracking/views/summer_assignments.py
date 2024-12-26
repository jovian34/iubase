from django.shortcuts import render
from django.db.models.functions import Lower

from player_tracking.models import SummerAssign, Accolade
from index.views import save_traffic_data


def view(request, summer_year):
    assignments = SummerAssign.objects.filter(summer_year=summer_year).order_by(
        Lower("player__last")
    )
    accolades = Accolade.objects.filter(summer_assign__isnull=False)
    context = {
        "page_title": f"{summer_year} College Summer League Assignments for current and former Indiana players",
        "assignments": assignments,
        "accolades": accolades,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/summer_assignments.html", context)