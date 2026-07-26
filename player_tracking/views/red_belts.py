from django import shortcuts
from django.contrib.auth import decorators as auth
from django.core.exceptions import PermissionDenied


@auth.login_required
def view(request):
    if not request.user.has_perm("player_tracking.add_accolade"):
        raise PermissionDenied

    context = {
        "page_title": "Red Belts",
    }
    return shortcuts.render(request, "player_tracking/red_belts.html", context)
