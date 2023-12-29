from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from live_game_blog.models import Game, Team, Scoreboard, BlogEntry


def games(request):
    finals = Scoreboard.objects.filter(game_status="final")
    final_pks = [ final.game.pk for final in finals ]
    games = Game.objects.exclude(pk__in=final_pks).order_by("first_pitch")[:3]
    context = { 
        "page_title": "iubase.com Live Game Blog Games",
        "games": games,
        }
    return render(request, "live_game_blog/games.html", context)

def past_games(request):
    scoreboards = Scoreboard.objects.select_related("game").filter(game_status="final").order_by("-update_time")
    context = { 
        "scoreboards": scoreboards,
        }
    return render(request, "live_game_blog/partials/past_games.html", context)

def live_game_blog(request, game_pk):
    game = Game.objects.get(pk=game_pk)
    blog_entries = BlogEntry.objects.filter(game=game).select_related("scoreboard").order_by("-blog_time")
    last_score = Scoreboard.objects.filter(game=game).order_by("-update_time")[0]
    context = {
        "entries": blog_entries,
        "game": game,
        "last_score": last_score,
    }
    return render(request, "live_game_blog/live_game_blog.html", context)

@login_required
def edit_live_game_blog(request, game_pk):
    game = Game.objects.get(pk=game_pk)
    blog_entries = BlogEntry.objects.filter(game=game).select_related("scoreboard").order_by("-blog_time")
    last_score = Scoreboard.objects.filter(game=game).order_by("-update_time")[0]
    context = {
        "entries": blog_entries,
        "game": game,
        "last_score": last_score,
    }
    return render(request, "live_game_blog/edit_live_game_blog.html", context)


