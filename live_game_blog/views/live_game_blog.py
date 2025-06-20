from django import shortcuts
from django import http

from index.views import save_traffic_data
from live_game_blog import models as lgb_models


def view(request, game_pk):
    game = get_game_or_raise_404(game_pk)
    game_over = is_game_over(game_pk)
    spring_year = set_spring_year(game)
    set_roster_url_to_game_year(game, spring_year)
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


def set_spring_year(game):
    spring_year = game.first_pitch.year
    if game.first_pitch.month > 7:
        spring_year += 1
    return spring_year


def set_roster_url_to_game_year(game, spring_year):
    if game.away_team.roster[-1] != "/":
        game.away_team.roster += f"/"
    if game.home_team.roster[-1] != "/":
        game.home_team.roster += f"/"

    if game.away_team.roster[-7:] == "season/":
        game.away_team.roster += f"{spring_year - 1}-{spring_year - 2000}"
    else:
        game.away_team.roster += f"{spring_year}/"

    if game.home_team.roster[-7:] == "season/":
        game.home_team.roster += f"{spring_year - 1}-{spring_year - 2000}"
    else:
        game.home_team.roster += f"{spring_year}/"


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
    latest_scoreboard = lgb_models.Scoreboard.objects.filter(game=game_pk).order_by(
        "-update_time"
    )[0]
    if latest_scoreboard.game_status in ["final", "cancelled", "post-game"]:
        return True
    return False
