from django import http, shortcuts, urls
from django.contrib.auth import decorators as auth

from live_game_blog import forms as lgb_forms
from live_game_blog import models as lgb_models


@auth.login_required
def view(request):
    if not request.user.has_perm("live_game_blog.add_game"):
        return http.HttpResponseForbidden()
    elif request.method == "POST":
        return validate_and_save_posted_game_form_then_redirect(request)
    else:
        return render_add_game_form_in_template(request)


def validate_and_save_posted_game_form_then_redirect(request):
    form = lgb_forms.AddGameForm(request.POST)
    if form.is_valid():
        save_game(form)
        this_game = save_initial_scoreboard(request)
    return shortcuts.redirect(urls.reverse("live_game_blog", args=[this_game.pk]))


def save_game(form):
    add_game = lgb_models.Game(
        home_team=form.cleaned_data["home_team"],
        home_rank=form.cleaned_data["home_rank"],
        home_seed=form.cleaned_data["home_seed"],
        home_nat_seed=form.cleaned_data["home_nat_seed"],
        away_team=form.cleaned_data["away_team"],
        away_rank=form.cleaned_data["away_rank"],
        away_seed=form.cleaned_data["away_seed"],
        away_nat_seed=form.cleaned_data["away_nat_seed"],
        neutral_site=form.cleaned_data["neutral_site"],
        event=form.cleaned_data["event"],
        featured_image=form.cleaned_data["featured_image"],
        live_stats=form.cleaned_data["live_stats"],
        video=form.cleaned_data["video"],
        video_url=form.cleaned_data["video_url"],
        audio_primary=form.cleaned_data["audio_primary"],
        audio_student=form.cleaned_data["audio_student"],
        first_pitch=form.cleaned_data["first_pitch"],
    )
    add_game.save()


def save_initial_scoreboard(request):
    this_game = lgb_models.Game.objects.last()
    add_initial_scoreboard = lgb_models.Scoreboard(
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
    return this_game


def render_add_game_form_in_template(request):
    context = {
        "form": lgb_forms.AddGameForm(),
        "page_title": "Add Game",
    }
    template_path = "live_game_blog/add_game.html"
    return shortcuts.render(request, template_path, context)
