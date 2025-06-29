from django.contrib.auth import decorators as auth
from django import http, shortcuts, urls

from datetime import date

from player_tracking.forms import SummerAssignForm
from player_tracking.models import Player, SummerAssign


@auth.login_required
def view(request, player_id):
    if not request.user.has_perm("player_tracking.add_summerassign"):
        return http.HttpResponseForbidden()
    elif request.method == "POST":
        form = SummerAssignForm(request.POST)
        if form.is_valid():
            save_summer_assign(player_id, form)
        return shortcuts.redirect(urls.reverse("single_player_page", args=[player_id]))
    else:
        form = SummerAssignForm(
            initial={
                "summer_year": date.today().year,
            },
        )
        context = {
            "player_id": player_id,
            "form": form,
        }
        return shortcuts.render(
            request,
            "player_tracking/partials/add_summer_assignment.html",
            context,
        )


def save_summer_assign(player_id, form):
    add_assign = SummerAssign.objects.create(
        player=Player.objects.get(pk=player_id),
        summer_year=form.cleaned_data["summer_year"],
        summer_league=form.cleaned_data["summer_league"],
        summer_team=form.cleaned_data["summer_team"],
        source=form.cleaned_data["source"],
        citation=form.cleaned_data["citation"],
    )
    add_assign.save()
