from django import shortcuts
from django import http

from index.views import save_traffic_data
from live_game_blog import models as lgb_models


def view(request, game_pk):
    game = get_game_or_raise_404(game_pk)
    game_over = is_game_over(game_pk)
    context = {
        "game": game,
        "entries": get_blog_entries(game_pk, game_over),
        "last_score": lgb_models.Scoreboard.objects.filter(game=game_pk).order_by(
            "-update_time"
        )[0],
        "game_over": game_over,
    }
    template_path = "live_game_blog/live_game_blog.html"
    save_traffic_data(request=request, page=context["game"].__str__())
    return shortcuts.render(request, template_path, context)


def get_blog_entries(game_pk, game_over):
    if game_over:
        blog_entries = lgb_models.BlogEntry.objects.filter(game=game_pk).order_by(
            "blog_time"
        )
    else:
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


def is_game_over(game_pk):
    latest_scoreboard = lgb_models.Scoreboard.objects.filter(game=game_pk).order_by("-update_time")[0]
    if latest_scoreboard.game_status in ["final", "cancelled", "post-game"]:
        return True
    return False