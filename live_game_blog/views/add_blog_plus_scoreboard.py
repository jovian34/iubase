from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from live_game_blog.forms import BlogAndScoreboardForm
from live_game_blog.models import BlogEntry, Game, Scoreboard


@login_required
def view(request, game_pk):
    if request.method == "POST":
        form = BlogAndScoreboardForm(request.POST)
        if form.is_valid():
            save_scoreboard(request, game_pk, form)
            save_blog_entry(request, game_pk, form)
        return redirect(reverse("edit_live_game_blog", args=[game_pk]))
    else:
        form = fill_initial_blog_and_scoreboard(game_pk)
        context = {"form": form, "game_pk": game_pk}
        return render(
            request, "live_game_blog/partials/add_blog_plus_scoreboard.html", context
        )


def save_scoreboard(request, game_pk, form):
    add_scoreboard = Scoreboard(
        game=Game.objects.get(pk=game_pk),
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
    this_score = Scoreboard.objects.filter(game=game_pk).last()
    add_blog = BlogEntry(
        game=Game.objects.get(pk=game_pk),
        author=request.user,
        blog_entry=form.cleaned_data["blog_entry"],
        include_scoreboard=True,
        scoreboard=Scoreboard.objects.get(pk=this_score.pk),
    )
    add_blog.save()


def fill_initial_blog_and_scoreboard(game_pk):
    last_score = Scoreboard.objects.filter(game=game_pk).last()
    inning = last_score.inning_num
    outs = last_score.outs
    part = last_score.inning_part
    if last_score.outs == 3 and last_score.inning_part == "Bottom":
        outs, inning, part = 0, last_score.inning_num + 1, "Top"
    elif last_score.outs == 3 and last_score.inning_part == "Top":
        outs, part = 0, "Bottom"
    form = BlogAndScoreboardForm(
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

    return form
