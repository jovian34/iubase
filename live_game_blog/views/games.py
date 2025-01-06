from django import shortcuts, urls
from django.db import models as db_models

from index.views import save_traffic_data
from live_game_blog import models as lgb_models


def upcoming(request):
    context = get_upcoming_games()
    template_path = "live_game_blog/games.html"
    save_traffic_data(request=request, page=context["page_title"])
    return shortcuts.render(request, template_path, context)


def get_upcoming_games():
    finals = lgb_models.Scoreboard.objects.filter(
        db_models.Q(game_status="final")
        | db_models.Q(game_status="cancelled")
        | db_models.Q(game_status="post-game")
    )
    final_pks = [final.game.pk for final in finals]
    context = {
        "page_title": "iubase.com Live Game Blog Games",
        "games": lgb_models.Game.objects.exclude(pk__in=final_pks).order_by(
            "first_pitch"
        )[:3],
    }
    return context


def past(request):
    if request.META.get("HTTP_HX_REQUEST"):
        context = {
            "scoreboards": lgb_models.Scoreboard.objects.select_related("game")
            .filter(game_status="final")
            .order_by("-update_time"),
        }
        template_path = "live_game_blog/partials/past_games.html"
        return shortcuts.render(request, template_path, context)
    else:
        return shortcuts.redirect(urls.reverse("games"))
