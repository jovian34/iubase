from django import http, shortcuts
from django.contrib.auth import decorators as auth

from player_tracking.logic.player_props import set_player_props_get_errors
from player_tracking.models import Player


@auth.login_required
def view(request):
    if not request.user.has_perm("player_tracking.change_player"):
        return http.HttpResponseForbidden()
    else:
        errors = set_player_props_get_errors()
        players_updated = Player.objects.all().order_by("last")
        context = {
            "players": players_updated,
            "error_exists": bool(len(errors)),
            "errors": errors,
            "page_title": "Errors From Last Spring Calculations",
        }
        return shortcuts.render(
            request, "player_tracking/calc_last_spring.html", context
        )


