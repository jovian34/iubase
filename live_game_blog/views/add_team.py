from django import shortcuts, urls
from django.contrib.auth import decorators as auth

from live_game_blog import forms as lgb_forms
from live_game_blog import models as lgb_models


@auth.permission_required("live_game_blog.add_team")
def view(request):
    if request.method == "POST":
        return validate_posted_add_team_form_save_then_redirect(request)
    else:
        return initialize_blank_add_team_form_and_render_template(request)


def validate_posted_add_team_form_save_then_redirect(request):
    form = lgb_forms.AddTeamForm(request.POST)
    if form.is_valid():
        save_team(form)
    return shortcuts.redirect(urls.reverse("games"))


def save_team(form):
    add_team = lgb_models.Team(
        team_name=form.cleaned_data["team_name"],
        mascot=form.cleaned_data["mascot"],
        logo=form.cleaned_data["logo"],
        stats=form.cleaned_data["stats"],
        roster=form.cleaned_data["roster"],
    )
    add_team.save()


def initialize_blank_add_team_form_and_render_template(request):
    context = {
        "form": lgb_forms.AddTeamForm(),
        "page_title": "Add Team",
    }
    template_path = "live_game_blog/add_team.html"
    return shortcuts.render(request, template_path, context)
