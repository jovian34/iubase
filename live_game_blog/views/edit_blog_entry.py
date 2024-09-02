from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from live_game_blog.models import Game, Scoreboard, BlogEntry
from live_game_blog.forms import (
    BlogAndScoreboardForm,
    BlogEntryForm,
)


@login_required
def view(request, entry_pk):
    edit_entry = BlogEntry.objects.get(pk=entry_pk)
    if edit_entry.include_scoreboard:
        edit_scoreboard = edit_entry.scoreboard
        if request.method == "POST":
            form = BlogAndScoreboardForm(request.POST)
            if form.is_valid():
                save_blog_entry_plus_scoreboard_edit(edit_entry, edit_scoreboard, form)
            return redirect(reverse("edit_live_game_blog", args=[edit_entry.game.pk]))
        else:
            form = current_blog_entry_plus_scoreboard_data(edit_entry, edit_scoreboard)
        context = {"form": form, "entry_pk": entry_pk}
        return render(request, "live_game_blog/partials/edit_blog_entry.html", context)
    else:
        if request.method == "POST":
            save_blog_only_entry(request, edit_entry)
            return redirect(reverse("edit_live_game_blog", args=[edit_entry.game.pk]))
        else:
            form = current_blog_only_entry(edit_entry)
            context = {"form": form, "entry_pk": entry_pk}
            return render(
                request, "live_game_blog/partials/edit_blog_entry.html", context
            )
        

def save_blog_entry_plus_scoreboard_edit(edit_entry, edit_scoreboard, form):
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


def current_blog_entry_plus_scoreboard_data(edit_entry, edit_scoreboard):
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
    
    return form


def save_blog_only_entry(request, edit_entry):
    form = BlogEntryForm(request.POST)
    if form.is_valid():
        edit_entry.blog_entry = form.cleaned_data["blog_entry"]
        edit_entry.is_raw_html = form.cleaned_data["is_raw_html"]
        edit_entry.save()


def current_blog_only_entry(edit_entry):
    form = BlogEntryForm(
                initial={
                    "blog_entry": edit_entry.blog_entry,
                    "is_raw_html": edit_entry.is_raw_html,
                }
            )
    
    return form
