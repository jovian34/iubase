from django import http, shortcuts, urls

from live_game_blog import forms as lgb_forms
from live_game_blog import models as lgb_models


def view(request, game_pk):
    if not request.user.has_perm("live_game_blog.add_blogentry"):
        return http.HttpResponseForbidden()
    elif request.method == "POST":
        return get_posted_form_to_save_blog_and_scoreboard_then_redirect(
            request, game_pk
        )
    else:
        context = {
            "form": fill_initial_blog_and_scoreboard(game_pk),
            "game_pk": game_pk,
        }
        template_path = "live_game_blog/partials/add_blog_plus_scoreboard.html"
        return shortcuts.render(request, template_path, context)


def get_posted_form_to_save_blog_and_scoreboard_then_redirect(request, game_pk):
    form = lgb_forms.BlogAndScoreboardForm(request.POST)
    if form.is_valid():
        save_scoreboard(request, game_pk, form)
        save_blog_entry(request, game_pk, form)
    return shortcuts.redirect(urls.reverse("live_game_blog", args=[game_pk]))


def save_scoreboard(request, game_pk, form):
    add_scoreboard = lgb_models.Scoreboard(
        game=lgb_models.Game.objects.get(pk=game_pk),
        scorekeeper=request.user,
        game_status=form.cleaned_data["game_status"],
        inning_num=form.cleaned_data["inning_num"],
        inning_part=form.cleaned_data["inning_part"],
        outs=form.cleaned_data["outs"],
        home_runs=form.cleaned_data["home_runs"],
        away_runs=form.cleaned_data["away_runs"],
        home_hits=form.cleaned_data["home_hits"],
        away_hits=form.cleaned_data["away_hits"],
        home_errors=form.cleaned_data["home_errors"],
        away_errors=form.cleaned_data["away_errors"],
    )
    add_scoreboard.save()


def save_blog_entry(request, game_pk, form):
    this_score = lgb_models.Scoreboard.objects.filter(game=game_pk).last()
    add_blog = lgb_models.BlogEntry(
        game=lgb_models.Game.objects.get(pk=game_pk),
        author=request.user,
        blog_entry=form.cleaned_data["blog_entry"],
        include_scoreboard=True,
        scoreboard=lgb_models.Scoreboard.objects.get(pk=this_score.pk),
    )
    add_blog.save()


def fill_initial_blog_and_scoreboard(game_pk):
    last_score = lgb_models.Scoreboard.objects.filter(game=game_pk).last()
    inning, outs, part = set_initial_inning_outs_and_part(last_score)
    return lgb_forms.BlogAndScoreboardForm(
        initial={
            "game_status": last_score.game_status,
            "inning_num": inning,
            "inning_part": part,
            "outs": outs,
            "home_runs": last_score.home_runs,
            "away_runs": last_score.away_runs,
            "home_hits": last_score.home_hits,
            "away_hits": last_score.away_hits,
            "home_errors": last_score.home_errors,
            "away_errors": last_score.away_errors,
        },
    )


def set_initial_inning_outs_and_part(last_score):
    if last_score.outs == 3 and last_score.inning_part == "Bottom":
        outs, inning, part = 0, last_score.inning_num + 1, "Top"
    elif last_score.outs == 3 and last_score.inning_part == "Top":
        outs, inning, part = 0, last_score.inning_num, "Bottom"
    else:
        outs, inning, part = (
            last_score.outs,
            last_score.inning_num,
            last_score.inning_part,
        )
    return inning, outs, part
