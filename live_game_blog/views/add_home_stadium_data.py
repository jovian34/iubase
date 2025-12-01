from django import shortcuts, http

from live_game_blog import models as lgb_models
from live_game_blog import forms


def view(request, team_pk):
    if not request.user.has_perm("live_game_blog.add_stadium"):
        return http.HttpResponseForbidden()
    team = lgb_models.Team.objects.get(pk=team_pk)
    template_path = "live_game_blog/add_home_stadium_data.html"
    context = {
        "team": team,
        "page_title": f"Add Home Stadium Data for {team.team_name}",
        "form": forms.AddHomeStadiumDataForm,
    }
    return shortcuts.render(request, template_path, context)