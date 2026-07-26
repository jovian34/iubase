from django import http, shortcuts
from django.contrib.auth import decorators as auth

from player_tracking.forms import SummerAssignForm
from player_tracking.models import SummerAssign
from player_tracking.views import single_player_page


@auth.login_required
def view(request, assignment_id):
    if not request.user.has_perm("player_tracking.change_summerassign"):
        return http.HttpResponseForbidden()

    assignment = shortcuts.get_object_or_404(SummerAssign, pk=assignment_id)
    if request.method == "POST":
        form = SummerAssignForm(request.POST)
        if form.is_valid():
            update_summer_assignment_from_form(assignment, form)
            return render_updated_summer_ball_or_redirect(request, assignment)
    else:
        form = initialize_summer_assignment_form(assignment)

    context = {
        "form": form,
        "assignment": assignment,
    }
    return shortcuts.render(
        request,
        "player_tracking/partials/edit_summer_assignment.html",
        context,
    )


def initialize_summer_assignment_form(assignment):
    return SummerAssignForm(
        initial={
            "summer_year": assignment.summer_year,
            "summer_league": assignment.summer_league,
            "summer_team": assignment.summer_team,
            "source": assignment.source,
            "citation": assignment.citation,
        }
    )


def update_summer_assignment_from_form(assignment, form):
    assignment.summer_year = form.cleaned_data["summer_year"]
    assignment.summer_league = form.cleaned_data["summer_league"]
    assignment.summer_team = form.cleaned_data["summer_team"]
    assignment.source = form.cleaned_data["source"]
    assignment.citation = form.cleaned_data["citation"]
    assignment.save()


def render_updated_summer_ball_or_redirect(request, assignment):
    if single_player_page.is_htmx_request(request):
        return single_player_page.render_player_section(
            request,
            assignment.player_id,
            "player_tracking/partials/player_summer_ball.html",
        )
    return shortcuts.redirect("single_player_page", player_id=assignment.player_id)
