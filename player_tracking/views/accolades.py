from django import shortcuts

from player_tracking import models as pt_models

def view(request):
    accolades = pt_models.Accolade.objects.all().order_by("-award_date")
    context = {
        "page_title": "Accolades",
        "accolades": accolades,
    }
    return shortcuts.render(request, "player_tracking/accolades.html", context)