from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Game, Team, Update


def games(request):
    games = Game.objects.exclude(inning_part="final").order_by("first_pitch")
    context = { 
        "page_title": "iubase.com Live Game Blog Games",
        "games": games,
        }
    return render(request, "live_game_blog/games.html", context)


def team_logo(request, team_pk):
    team = Team.objects.get(pk=team_pk)
    context = { "team": team }
    return render(request, "live_game_blog/partials/team_logo.html", context)

def past_games(request):
    games = Update.objects.select_related("game").filter(inning_part="final").order_by("-update_time")
    context = { 
        "games": games,
        }
    return render(request, "live_game_blog/partials/past_games.html", context)

def live_game_blog(request, game_pk):
    game = Game.objects.get(pk=game_pk)
    blog_entries = Update.objects.filter(game=game_pk).order_by("-blog_time")
    context = {
        "entries": blog_entries,
        "game": game,
    }
    return render(request, "live_game_blog/live_game_blog.html", context)