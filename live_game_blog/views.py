from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import timedelta

from accounts.models import CustomUser
from live_game_blog.models import Game, Team, Scoreboard, BlogEntry
from live_game_blog.forms import BlogAndScoreboardForm, BlogEntryForm, AddGameForm, AddTeamForm


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


@login_required
def add_blog_entry_only(request, game_pk):
    if request.method == "POST":
        form = BlogEntryForm(request.POST)
        if form.is_valid():
            add_blog = BlogEntry(
                game=Game.objects.get(pk=game_pk),
                author=request.user,
                blog_entry=form.cleaned_data["blog_entry"],
                is_raw_html=form.cleaned_data["is_raw_html"],
                include_scoreboard=False,
            )
            add_blog.save()
            if form.cleaned_data["is_x_embed"]:
                iubase17 = CustomUser.objects.filter(username="iubase17")[0]
                add_blog.author=iubase17
                add_blog.save()            
        return redirect(reverse("edit_live_game_blog", args=[game_pk]))
    else:
        form = BlogEntryForm()
        context = { "form": form, "game_pk": game_pk }
        print("rendering form to add blog only")
        return render(request, "live_game_blog/partials/add_blog_entry_only.html", context)
    

@login_required
def add_blog_plus_scoreboard(request, game_pk):
    if request.method == "POST":
        form = BlogAndScoreboardForm(request.POST)
        if form.is_valid():
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
            this_score = Scoreboard.objects.filter(game=game_pk).last()
            add_blog = BlogEntry(
                game=Game.objects.get(pk=game_pk),
                author=request.user,
                blog_entry=form.cleaned_data["blog_entry"],
                include_scoreboard=True,
                scoreboard=Scoreboard.objects.get(pk=this_score.pk)
            )
            add_blog.save()
        return redirect(reverse("edit_live_game_blog", args=[game_pk]))
    else:
        last_score = Scoreboard.objects.filter(game=game_pk).last()
        game = Game.objects.get(pk=game_pk)
        away = game.away_team.mascot
        home = game.home_team.mascot
        if last_score.outs == 3:
            outs = 0
            inning = last_score.inning_num + 1
        else:
            outs = last_score.outs
            inning = last_score.inning_num
        form = BlogAndScoreboardForm(
            initial={
                "game_status": last_score.game_status,
                "inning_num": inning,
                "inning_part": last_score.inning_part,
                "outs": outs,
                "home_runs": last_score.home_runs,
                "away_runs": last_score.away_runs,
                "home_hits": last_score.home_hits,
                "away_hits": last_score.away_hits,
                "home_errors": last_score.home_errors,
                "away_errors": last_score.away_errors,
            },
        )        
        context = { "form": form, "game_pk": game_pk }
        return render(request, "live_game_blog/partials/add_blog_plus_scoreboard.html", context)
    

@login_required
def add_game(request):
    print(request.POST)
    if request.method == "POST":
        form = AddGameForm(request.POST)
        if form.is_valid():
            add_game = Game(
                home_team=form.cleaned_data["home_team"],
                away_team=form.cleaned_data["away_team"],
                neutral_site=form.cleaned_data["neutral_site"],
                live_stats=form.cleaned_data["live_stats"],
                first_pitch=form.cleaned_data["first_pitch"]
            )
            add_game.save()
            add_initial_scoreboard = Scoreboard(
                game_status="pre-game",
                game=Game.objects.filter(first_pitch=form.cleaned_data["first_pitch"])[0],
                scorekeeper=request.user,
            )
            add_initial_scoreboard.save()
        return redirect(reverse("edit_live_game_blog", args=[Game.objects.filter(first_pitch=form.cleaned_data["first_pitch"])[0].pk]))
    else:
        form = AddGameForm()
        context = { "form": form, "page_title": "Add Game", }
        return render(request, "live_game_blog/add_game_or_team.html", context)
    

@login_required
def add_team(request):
    if request.method == "POST":
        form = AddTeamForm(request.POST)
        if form.is_valid():
            add_team = Team(
                team_name=form.cleaned_data["team_name"],
                mascot=form.cleaned_data["mascot"],
                logo=form.cleaned_data["logo"],
                stats=form.cleaned_data["stats"],
                roster=form.cleaned_data["roster"]
            )
            add_team.save()
        return redirect(reverse("games"))
    else:
        form = AddTeamForm()
        context = { "form": form, "page_title": "Add Team", }
        return render(request, "live_game_blog/add_game_or_team.html", context)
