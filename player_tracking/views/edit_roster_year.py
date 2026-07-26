from django import http, shortcuts
from django.contrib.auth import decorators as auth

from player_tracking import forms
from player_tracking.models import AnnualRoster
from player_tracking.views import set_player_properties, single_player_page


@auth.login_required
def view(request, roster_id):
    if not request.user.has_perm("player_tracking.change_annualroster"):
        return http.HttpResponseForbidden()
    if not single_player_page.is_htmx_request(request):
        return http.HttpResponseBadRequest()

    roster = shortcuts.get_object_or_404(AnnualRoster, pk=roster_id)
    if request.method == "POST":
        form = forms.AnnualRosterForm(request.POST)
        if form.is_valid():
            update_roster_from_form(roster, form)
            return render_updated_rosters(request, roster)
    else:
        form = initialize_roster_form(roster)

    context = {
        "form": form,
        "roster": roster,
    }
    return shortcuts.render(
        request,
        "player_tracking/partials/edit_roster_year.html",
        context,
    )


def initialize_roster_form(roster):
    return forms.AnnualRosterForm(
        initial={
            "spring_year": roster.spring_year,
            "team": roster.team,
            "jersey": roster.jersey,
            "status": roster.status,
            "primary_position": roster.primary_position,
            "secondary_position": roster.secondary_position,
        }
    )


def update_roster_from_form(roster, form):
    roster.spring_year = form.cleaned_data["spring_year"]
    roster.team = form.cleaned_data["team"]
    roster.jersey = form.cleaned_data["jersey"]
    roster.status = form.cleaned_data["status"]
    roster.primary_position = form.cleaned_data["primary_position"]
    roster.secondary_position = form.cleaned_data["secondary_position"]
    roster.save()
    set_player_properties.set_player_props_get_errors()


def render_updated_rosters(request, roster):
    return single_player_page.render_player_section(
        request,
        roster.player_id,
        "player_tracking/partials/annual_rosters.html",
    )
