from django import shortcuts
from django.contrib.auth import decorators as auth

from live_game_blog import models as lgb_models


@auth.login_required
def view(request, game_pk):
    context = {
        "entries": get_blog_entries(game_pk),
        "game": lgb_models.Game.objects.get(pk=game_pk),
        "last_score": lgb_models.Scoreboard.objects.filter(game=game_pk).order_by(
            "-update_time"
        )[0],
    }
    template_path = "live_game_blog/edit_live_game_blog.html"
    return shortcuts.render(request, template_path, context)


def get_blog_entries(game_pk):
    return lgb_models.BlogEntry.objects.filter(game=game_pk).order_by("-blog_time")
