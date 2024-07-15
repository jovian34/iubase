from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q

from accounts.models import CustomUser
from index.views import save_traffic_data
from live_game_blog.models import Game, Team, Scoreboard, BlogEntry
from live_game_blog.forms import (
    BlogAndScoreboardForm,
    BlogEntryForm,
    AddGameForm,
    AddTeamForm,
)


def games(request):
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


def past_games(request):
    scoreboards = (
        Scoreboard.objects.select_related("game")
        .filter(game_status="final")
        .order_by("-update_time")
    )
    context = {
        "scoreboards": scoreboards,
    }
    return render(request, "live_game_blog/partials/past_games.html", context)


def live_game_blog(request, game_pk):
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
    save_traffic_data(request=request, page=game.__str__())
    return render(request, "live_game_blog/live_game_blog.html", context)


@login_required
def edit_live_game_blog(request, game_pk):
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
                add_blog.author = iubase17
                add_blog.save()
        return redirect(reverse("edit_live_game_blog", args=[game_pk]))
    else:
        form = BlogEntryForm()
        context = {"form": form, "game_pk": game_pk}
        print("rendering form to add blog only")
        return render(
            request, "live_game_blog/partials/add_blog_entry_only.html", context
        )


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
                scoreboard=Scoreboard.objects.get(pk=this_score.pk),
            )
            add_blog.save()
        return redirect(reverse("edit_live_game_blog", args=[game_pk]))
    else:
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
        context = {"form": form, "game_pk": game_pk}
        return render(
            request, "live_game_blog/partials/add_blog_plus_scoreboard.html", context
        )


@login_required
def edit_blog_entry(request, entry_pk):
    edit_entry = BlogEntry.objects.get(pk=entry_pk)
    if edit_entry.include_scoreboard:
        edit_scoreboard = edit_entry.scoreboard
        if request.method == "POST":
            form = BlogAndScoreboardForm(request.POST)
            if form.is_valid():
                edit_scoreboard.game_status = form.cleaned_data["game_status"]
                edit_scoreboard.inning_num = form.cleaned_data["inning_num"]
                edit_scoreboard.inning_part = form.cleaned_data["inning_part"]
                edit_scoreboard.outs = form.cleaned_data["outs"]
                edit_scoreboard.home_runs = form.cleaned_data["home_runs"]
                edit_scoreboard.away_runs = form.cleaned_data["away_runs"]
                edit_scoreboard.home_hits = form.cleaned_data["home_hits"]
                edit_scoreboard.away_hits = form.cleaned_data["away_hits"]
                edit_scoreboard.home_errors = form.cleaned_data["home_errors"]
                edit_scoreboard.away_errors = form.cleaned_data["away_errors"]
                edit_scoreboard.save()
                edit_entry.blog_entry = form.cleaned_data["blog_entry"]
                edit_entry.save()
            return redirect(reverse("edit_live_game_blog", args=[edit_entry.game.pk]))
        else:
            form = BlogAndScoreboardForm(
                initial={
                    "blog_entry": edit_entry.blog_entry,
                    "game_status": edit_scoreboard.game_status,
                    "inning_num": edit_scoreboard.inning_num,
                    "inning_part": edit_scoreboard.inning_part,
                    "outs": edit_scoreboard.outs,
                    "home_runs": edit_scoreboard.home_runs,
                    "away_runs": edit_scoreboard.away_runs,
                    "home_hits": edit_scoreboard.home_hits,
                    "away_hits": edit_scoreboard.away_hits,
                    "home_errors": edit_scoreboard.home_errors,
                    "away_errors": edit_scoreboard.away_errors,
                },
            )
        context = {"form": form, "entry_pk": entry_pk}
        return render(request, "live_game_blog/partials/edit_blog_entry.html", context)
    else:
        if request.method == "POST":
            form = BlogEntryForm(request.POST)
            if form.is_valid():
                edit_entry.blog_entry = form.cleaned_data["blog_entry"]
                edit_entry.is_raw_html = form.cleaned_data["is_raw_html"]
                edit_entry.save()
            return redirect(reverse("edit_live_game_blog", args=[edit_entry.game.pk]))
        else:
            form = BlogEntryForm(
                initial={
                    "blog_entry": edit_entry.blog_entry,
                    "is_raw_html": edit_entry.is_raw_html,
                }
            )

            context = {"form": form, "entry_pk": entry_pk}
            return render(
                request, "live_game_blog/partials/edit_blog_entry.html", context
            )


@login_required
def add_game(request):
    if request.method == "POST":
        form = AddGameForm(request.POST)
        if form.is_valid():
            add_game = Game(
                home_team=form.cleaned_data["home_team"],
                home_rank=form.cleaned_data["home_rank"],
                home_seed=form.cleaned_data["home_seed"],
                home_nat_seed=form.cleaned_data["home_nat_seed"],
                away_team=form.cleaned_data["away_team"],
                away_rank=form.cleaned_data["away_rank"],
                away_seed=form.cleaned_data["away_seed"],
                away_nat_seed=form.cleaned_data["away_nat_seed"],
                neutral_site=form.cleaned_data["neutral_site"],
                live_stats=form.cleaned_data["live_stats"],
                video=form.cleaned_data["video"],
                video_url=form.cleaned_data["video_url"],
                audio_primary=form.cleaned_data["audio_primary"],
                audio_student=form.cleaned_data["audio_student"],
                first_pitch=form.cleaned_data["first_pitch"],
            )
            add_game.save()
            this_game = Game.objects.last()
            add_initial_scoreboard = Scoreboard(
                game_status="pre-game",
                game=this_game,
                scorekeeper=request.user,
                inning_num=1,
                inning_part="Top",
                outs=0,
                home_runs=0,
                away_runs=0,
                home_hits=0,
                away_hits=0,
                home_errors=0,
                away_errors=0,
            )
            add_initial_scoreboard.save()
        return redirect(reverse("edit_live_game_blog", args=[this_game.pk]))
    else:
        form = AddGameForm()
        context = {
            "form": form,
            "page_title": "Add Game",
        }
        return render(request, "live_game_blog/add_game.html", context)


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
                roster=form.cleaned_data["roster"],
            )
            add_team.save()
        return redirect(reverse("games"))
    else:
        form = AddTeamForm()
        context = {
            "form": form,
            "page_title": "Add Team",
        }
        return render(request, "live_game_blog/add_team.html", context)
