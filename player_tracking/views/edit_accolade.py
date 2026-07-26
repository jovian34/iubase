from django import http, shortcuts
from django.contrib.auth import decorators as auth

from player_tracking.forms import AccoladeForm
from player_tracking.models import Accolade
from player_tracking.views import single_player_page


@auth.login_required
def view(request, accolade_id):
    if not request.user.has_perm("player_tracking.change_accolade"):
        return http.HttpResponseForbidden()

    accolade = shortcuts.get_object_or_404(Accolade, pk=accolade_id)
    if request.method == "POST":
        form = AccoladeForm(
            data=request.POST,
            player_id=accolade.player_id,
        )
        if form.is_valid():
            update_accolade_from_form(accolade, form)
            return render_updated_accolades_or_redirect(request, accolade)
    else:
        form = initialize_accolade_form(accolade)

    section_id, _ = get_accolade_section(accolade)
    context = {
        "accolade": accolade,
        "form": form,
        "section_id": section_id,
    }
    return shortcuts.render(
        request,
        "player_tracking/partials/edit_accolade.html",
        context,
    )


def initialize_accolade_form(accolade):
    return AccoladeForm(
        player_id=accolade.player_id,
        initial={
            "name": accolade.name,
            "award_date": accolade.award_date,
            "award_org": accolade.award_org,
            "description": accolade.description,
            "citation": accolade.citation,
            "annual_roster": accolade.annual_roster,
            "summer_assign": accolade.summer_assign,
        },
    )


def update_accolade_from_form(accolade, form):
    accolade.name = form.cleaned_data["name"]
    accolade.award_date = form.cleaned_data["award_date"]
    accolade.award_org = form.cleaned_data["award_org"]
    accolade.description = form.cleaned_data["description"]
    accolade.citation = form.cleaned_data["citation"]
    accolade.annual_roster = form.cleaned_data["annual_roster"]
    accolade.summer_assign = form.cleaned_data["summer_assign"]
    accolade.save()


def render_updated_accolades_or_redirect(request, accolade):
    if single_player_page.is_htmx_request(request):
        _, template_name = get_accolade_section(accolade)
        return single_player_page.render_player_section(
            request,
            accolade.player_id,
            template_name,
        )
    return shortcuts.redirect("single_player_page", player_id=accolade.player_id)


def get_accolade_section(accolade):
    if accolade.annual_roster_id:
        return "annual-rosters", "player_tracking/partials/annual_rosters.html"
    if accolade.summer_assign_id:
        return "summer-ball", "player_tracking/partials/player_summer_ball.html"
    return "other-accolades", "player_tracking/partials/other_accolades.html"
