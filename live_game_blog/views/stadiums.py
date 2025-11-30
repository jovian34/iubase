from django import shortcuts
from django.db.models import Q

from live_game_blog import models as lgb_models
from conference import models as conf_models

def view(request):
    template_path = "live_game_blog/stadiums.html"
    context = {
        "title": "Stadium Actions",
    }
    return shortcuts.render(request, template_path, context)


def teams_wo_stad_config(request):
    teams = lgb_models.Team.objects.filter(
        Q(homestadium__isnull=True)
    ).order_by("team_name")
    template_path = "live_game_blog/partials/teams_wo_stad_config.html"
    context = {
        "teams": teams,
    }
    return shortcuts.render(request, template_path, context)