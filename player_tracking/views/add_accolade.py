from django import http, shortcuts, urls
from django.contrib.auth import decorators as auth

from player_tracking import forms
from player_tracking import models as pt_models
from player_tracking.views import single_player_page


SECTION_TEMPLATES = {
    "annual-rosters": "player_tracking/partials/annual_rosters.html",
    "other-accolades": "player_tracking/partials/other_accolades.html",
}


@auth.login_required
def view(request, player_id):
    if not request.user.has_perm("player_tracking.add_accolade"):
        return http.HttpResponseForbidden()
    elif request.method == "POST":
        return validate_accolade_form_post_save_then_redirect(request, player_id)
    else:
        context = {
            "player_id": player_id,
            "form": forms.AccoladeForm(player_id=player_id),
            "target_section": get_target_section(request),
        }
        template_path = "player_tracking/partials/add_accolade.html"
        return shortcuts.render(request, template_path, context)


def validate_accolade_form_post_save_then_redirect(request, player_id):
    form = forms.AccoladeForm(player_id=player_id, data=request.POST)
    if form.is_valid():
        create_accolade_and_save(player_id, form)
        if single_player_page.is_htmx_request(request):
            return single_player_page.render_player_section(
                request,
                player_id,
                SECTION_TEMPLATES[get_target_section(request)],
            )
    return shortcuts.redirect(urls.reverse("single_player_page", args=[player_id]))


def get_target_section(request):
    target_section = request.POST.get(
        "target_section",
        request.META.get("HTTP_X_PLAYER_SECTION", "other-accolades"),
    )
    if target_section in SECTION_TEMPLATES:
        return target_section
    return "other-accolades"


def create_accolade_and_save(player_id, form):
    add_accolade = pt_models.Accolade.objects.create(
        player=pt_models.Player.objects.get(pk=player_id),
        name=form.cleaned_data["name"],
        award_date=form.cleaned_data["award_date"],
        award_org=form.cleaned_data["award_org"],
        description=form.cleaned_data["description"],
        citation=form.cleaned_data["citation"],
        annual_roster=form.cleaned_data["annual_roster"],
        summer_assign=form.cleaned_data["summer_assign"],
    )
    add_accolade.save()
