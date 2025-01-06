from django import shortcuts
from django import http

from index.views import save_traffic_data
from live_game_blog import models as lgb_models


def view(request, game_pk):
    context = {
        "game": get_game_or_raise_404(game_pk),
        "entries": get_blog_entries(game_pk),
        "last_score": lgb_models.Scoreboard.objects.filter(game=game_pk).order_by(
            "-update_time"
        )[0],
    }
    template_path = "live_game_blog/live_game_blog.html"
    save_traffic_data(request=request, page=context["game"].__str__())
    return shortcuts.render(request, template_path, context)


def get_blog_entries(game_pk):
    blog_entries = lgb_models.BlogEntry.objects.filter(game=game_pk).order_by(
        "-blog_time"
    )
    return blog_entries


def get_game_or_raise_404(game_pk):
    try:
        game = lgb_models.Game.objects.get(pk=game_pk)
    except lgb_models.Game.DoesNotExist:
        raise http.Http404
    return game
