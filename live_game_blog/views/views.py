from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q

from accounts.models import CustomUser
from index.views import save_traffic_data
from live_game_blog.models import Game, Scoreboard, BlogEntry
from live_game_blog.forms import BlogEntryForm


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