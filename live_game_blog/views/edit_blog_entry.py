from django.contrib.auth import decorators as auth
from django import http, urls, shortcuts

from live_game_blog import models as lgb_models
from live_game_blog import forms as lgb_forms


@auth.login_required
def view(request, entry_pk):
    if not request.user.has_perm("live_game_blog.change_gameblogentry"):
        return http.HttpResponseForbidden()
    edit_entry = lgb_models.BlogEntry.objects.get(pk=entry_pk)
    if edit_entry.include_scoreboard:
        return edit_blog_plus_scoreboard_entry(request, edit_entry)
    else:
        return edit_blog_only_entry(request, edit_entry)


def edit_blog_plus_scoreboard_entry(request, edit_entry):
    edit_scoreboard = edit_entry.scoreboard
    if request.method == "POST":
        validate_blog_and_score_form_and_save(request, edit_entry, edit_scoreboard)
        return shortcuts.redirect(
            urls.reverse("live_game_blog", args=[edit_entry.game.pk])
        )
    else:
        context = {
            "form": get_form_with_current_blog_entry_plus_scoreboard_data(
                edit_entry, edit_scoreboard
            ),
            "entry_pk": edit_entry.pk,
        }
        template_path = "live_game_blog/partials/edit_blog_entry.html"
        return shortcuts.render(request, template_path, context)


def validate_blog_and_score_form_and_save(request, edit_entry, edit_scoreboard):
    form = lgb_forms.BlogAndScoreboardForm(request.POST)
    if form.is_valid():
        save_blog_entry_plus_scoreboard_edit(edit_entry, edit_scoreboard, form)


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


def get_form_with_current_blog_entry_plus_scoreboard_data(edit_entry, edit_scoreboard):
    return lgb_forms.BlogAndScoreboardForm(
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


def edit_blog_only_entry(request, edit_entry):
    if request.method == "POST":
        save_blog_only_entry(request, edit_entry)
        return shortcuts.redirect(
            urls.reverse("live_game_blog", args=[edit_entry.game.pk])
        )
    else:
        context = {
            "form": get_form_with_current_blog_only_entry(edit_entry),
            "entry_pk": edit_entry.pk,
        }
        template_path = "live_game_blog/partials/edit_blog_entry.html"
        return shortcuts.render(request, template_path, context)


def save_blog_only_entry(request, edit_entry):
    form = lgb_forms.BlogEntryForm(request.POST)
    if form.is_valid():
        edit_entry.blog_entry = form.cleaned_data["blog_entry"]
        edit_entry.is_raw_html = form.cleaned_data["is_raw_html"]
        edit_entry.save()


def get_form_with_current_blog_only_entry(edit_entry):
    return lgb_forms.BlogEntryForm(
        initial={
            "blog_entry": edit_entry.blog_entry,
            "is_raw_html": edit_entry.is_raw_html,
        }
    )
