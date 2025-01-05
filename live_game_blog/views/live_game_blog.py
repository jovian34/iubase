from django.shortcuts import render
from django import http

from index.views import save_traffic_data
from live_game_blog.models import Game, Scoreboard, BlogEntry


def view(request, game_pk):
    try:
        game = Game.objects.get(pk=game_pk)
    except Game.DoesNotExist:
        raise http.Http404
    blog_entries = (
        BlogEntry.objects.filter(game=game)
        .select_related("scoreboard")
        .order_by("-blog_time")
    )
    last_score = Scoreboard.objects.filter(game=game).order_by("-update_time")[0]
    context = {
        "entries": blog_entries,
        "game": game,
        "last_score": last_score,
    }
    save_traffic_data(request=request, page=game.__str__())
    return render(request, "live_game_blog/live_game_blog.html", context)
