from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from live_game_blog.models import Game, Scoreboard, BlogEntry


@login_required
def view(request, game_pk):
    game = Game.objects.get(pk=game_pk)
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
    return render(request, "live_game_blog/edit_live_game_blog.html", context)