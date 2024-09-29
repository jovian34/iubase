from django.shortcuts import render, redirect
from django.db.models import Q

from index.views import save_traffic_data
from live_game_blog.models import Game, Scoreboard



def upcoming(request):
    finals = Scoreboard.objects.filter(
        Q(game_status="final") | Q(game_status="cancelled") | Q(game_status="post-game")
    )
    final_pks = [final.game.pk for final in finals]
    games = Game.objects.exclude(pk__in=final_pks).order_by("first_pitch")[:3]
    context = {
        "page_title": "iubase.com Live Game Blog Games",
        "games": games,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "live_game_blog/games.html", context)


def past(request):
    if request.META.get('HTTP_HX_REQUEST'):
        scoreboards = (
            Scoreboard.objects.select_related("game")
            .filter(game_status="final")
            .order_by("-update_time")
        )
        context = {
            "scoreboards": scoreboards,
        }
        return render(request, "live_game_blog/partials/past_games.html", context)
    else:
        return redirect("games")
