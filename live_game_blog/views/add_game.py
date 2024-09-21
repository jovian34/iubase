from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from live_game_blog.forms import AddGameForm
from live_game_blog.models import Game, Scoreboard


@login_required
def view(request):
    if request.method == "POST":
        form = AddGameForm(request.POST)
        if form.is_valid():
            save_game(form)
            this_game = save_initial_scoreboard(request)
        return redirect(reverse("edit_live_game_blog", args=[this_game.pk]))
    else:
        form = AddGameForm()
        context = {
            "form": form,
            "page_title": "Add Game",
        }
        return render(request, "live_game_blog/add_game.html", context)
    

def save_game(form):
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
                fall_exhibition=form.cleaned_data["fall_exhibition"],
                live_stats=form.cleaned_data["live_stats"],
                video=form.cleaned_data["video"],
                video_url=form.cleaned_data["video_url"],
                audio_primary=form.cleaned_data["audio_primary"],
                audio_student=form.cleaned_data["audio_student"],
                first_pitch=form.cleaned_data["first_pitch"],
            )
    add_game.save()
    

def save_initial_scoreboard(request):
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
    return this_game