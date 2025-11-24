from django.contrib.auth import decorators as auth
from django import http, shortcuts, urls

from live_game_blog import forms as lgb_forms
from live_game_blog import models as lgb_models


@auth.login_required
def view(request, game_pk):
    if not request.user.has_perm("live_game_blog.change_game"):
        return http.HttpResponseForbidden()
    edit_game = lgb_models.Game.objects.get(pk=game_pk)
    if request.method == "POST":
        form = lgb_forms.AddGameForm(request.POST)
        if form.is_valid():
            save_edited_game(edit_game, form)
        return shortcuts.redirect(
            urls.reverse("live_game_blog", args=[game_pk])
        )
    else:        
        context = {
            "form": get_form_with_current_game_info(edit_game),
            "game_pk": game_pk,
        }
        template_path = "live_game_blog/partials/edit_game_info.html"
        return shortcuts.render(request, template_path, context)
    

def get_form_with_current_game_info(edit_game):
    return lgb_forms.AddGameForm(
        initial={
            "home_team": edit_game.home_team,
            "away_team": edit_game.away_team,
            "first_pitch": edit_game.first_pitch,
            "event": edit_game.event,
            "home_rank": edit_game.home_rank,
            "home_seed": edit_game.home_seed,
            "home_nat_seed": edit_game.home_nat_seed,
            "away_rank": edit_game.away_rank,
            "away_seed": edit_game.away_seed,
            "away_nat_seed": edit_game.away_nat_seed,
            "featured_image": edit_game.featured_image,
            "live_stats": edit_game.live_stats,
            "video": edit_game.video,
            "video_url": edit_game.video_url,
            "audio_primary": edit_game.audio_primary,
            "audio_student": edit_game.audio_student,
            "first_pitch_temp": edit_game.first_pitch_temp,
            "first_pitch_wind_speed": edit_game.first_pitch_wind_speed,
            "first_pitch_wind_angle": edit_game.first_pitch_wind_angle,
        }
    )
    


def save_edited_game(edit_game, form):
    edit_game.home_team = form.cleaned_data["home_team"]
    edit_game.home_rank = form.cleaned_data["home_rank"]
    edit_game.home_seed = form.cleaned_data["home_seed"]
    edit_game.home_nat_seed = form.cleaned_data["home_nat_seed"]
    edit_game.away_team = form.cleaned_data["away_team"]
    edit_game.away_rank = form.cleaned_data["away_rank"]
    edit_game.away_seed = form.cleaned_data["away_seed"]
    edit_game.away_nat_seed = form.cleaned_data["away_nat_seed"]
    edit_game.event = form.cleaned_data["event"]
    edit_game.featured_image = form.cleaned_data["featured_image"]
    edit_game.live_stats = form.cleaned_data["live_stats"]
    edit_game.video = form.cleaned_data["video"]
    edit_game.video_url = form.cleaned_data["video_url"]
    edit_game.audio_primary = form.cleaned_data["audio_primary"]
    edit_game.audio_student = form.cleaned_data["audio_student"]
    edit_game.first_pitch = form.cleaned_data["first_pitch"]
    edit_game.first_pitch_temp = form.cleaned_data["first_pitch_temp"]
    edit_game.first_pitch_wind_speed = form.cleaned_data["first_pitch_wind_speed"]
    edit_game.first_pitch_wind_angle = form.cleaned_data["first_pitch_wind_angle"]
    edit_game.save()