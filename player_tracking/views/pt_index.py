from django.shortcuts import render

from datetime import date
from index.views import save_traffic_data


def view(request):
    context = {
        "page_title": "Player Tracking",
        "this_year": str(date.today().year),
        "last_year": str(date.today().year - 1),
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/pt_index.html", context)
