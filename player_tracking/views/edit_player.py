from django import http, shortcuts, urls
from django.contrib.auth import decorators as auth

from player_tracking.models import Player
from player_tracking import forms


@auth.login_required
def view(request, player_id):
    if not request.user.has_perm("player_tracking.change_player"):
        return http.HttpResponseForbidden()
    edit_info = Player.objects.get(pk=player_id)
    if request.method == "POST":
        validate_form_and_save_data(request, edit_info)
        return shortcuts.redirect(urls.reverse("single_player_page", args=[player_id]))
    else:
        context = {
            "form": initialize_form_with_existing_data(edit_info),
            "player_id": player_id,
        }
        template_path = "player_tracking/partials/edit_player.html"
        return shortcuts.render(request, template_path, context)
    

def initialize_form_with_existing_data(edit_info):
    form = forms.PlayerForm(
            initial={
                "first": edit_info.first,
                "last": edit_info.last,
                "hsgrad_year": edit_info.hsgrad_year,
                "high_school": edit_info.high_school,
                "home_city": edit_info.home_city,
                "home_state": edit_info.home_state,
                "home_country": edit_info.home_country,
                "headshot": edit_info.headshot,
                "action_shot": edit_info.action_shot,
                "birthdate": edit_info.birthdate,
                "bats": edit_info.bats,
                "throws": edit_info.throws,
                "height": edit_info.height,
                "weight": edit_info.weight,
                "primary_position": edit_info.primary_position,
            },
        )    
    return form


def validate_form_and_save_data(request, edit_info):
    form = forms.PlayerForm(request.POST)
    if form.is_valid():
        edit_info.first = form.cleaned_data["first"]
        edit_info.last = form.cleaned_data["last"]
        edit_info.hsgrad_year = form.cleaned_data["hsgrad_year"]
        edit_info.high_school = form.cleaned_data["high_school"]
        edit_info.home_city = form.cleaned_data["home_city"]
        edit_info.home_state = form.cleaned_data["home_state"]
        edit_info.home_country = form.cleaned_data["home_country"]
        edit_info.headshot = form.cleaned_data["headshot"]
        edit_info.action_shot = form.cleaned_data["action_shot"]
        edit_info.birthdate = form.cleaned_data["birthdate"]
        edit_info.bats = form.cleaned_data["bats"]
        edit_info.throws = form.cleaned_data["throws"]
        edit_info.height = form.cleaned_data["height"]
        edit_info.weight = form.cleaned_data["weight"]
        edit_info.primary_position = form.cleaned_data["primary_position"]
        edit_info.save()
