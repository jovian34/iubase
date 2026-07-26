from django import shortcuts
from django.contrib.auth import decorators as auth
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404
from django.utils import timezone

from player_tracking import choices, forms
from player_tracking import models as pt_models


@auth.login_required
def redirect_to_current_year(request):
    require_add_accolade_permission(request)
    return shortcuts.redirect("red_belt_entry", spring_year=timezone.localdate().year)


@auth.login_required
def view(request, spring_year):
    require_add_accolade_permission(request)
    spring_year = int(spring_year)
    if spring_year > timezone.localdate().year:
        raise Http404

    form = forms.RedBeltEntryForm(
        request.POST or None,
        spring_year=spring_year,
    )
    if request.method == "POST" and form.is_valid():
        save_weekly_red_belts(form)
        return shortcuts.redirect("red_belt_entry", spring_year=spring_year)

    context = {
        "form": form,
        "page_title": f"Weekly Red Belt Entry for {spring_year}",
        "spring_year": spring_year,
        "years": get_spring_roster_years(),
    }
    if request.META.get("HTTP_HX_REQUEST"):
        template_path = "player_tracking/partials/red_belt_entry_form.html"
    else:
        template_path = "player_tracking/red_belt_entry.html"
    return shortcuts.render(request, template_path, context)


def require_add_accolade_permission(request):
    if not request.user.has_perm("player_tracking.add_accolade"):
        raise PermissionDenied


def get_spring_roster_years():
    return (
        pt_models.AnnualRoster.objects.filter(
            spring_year__lte=timezone.localdate().year,
            team__team_name="Indiana",
            status__in=choices.ALL_ROSTER,
        )
        .order_by("-spring_year")
        .values_list("spring_year", flat=True)
        .distinct()
    )


@transaction.atomic
def save_weekly_red_belts(form):
    award_date = form.cleaned_data["award_date"]
    awards = (
        (
            "Joey DeNato Weekly Red Belt for pitching",
            form.cleaned_data["pitcher"],
        ),
        (
            "Alex Dickerson Weekly Red Belt for hitting",
            form.cleaned_data["hitter"],
        ),
        (
            "Tony Butler Weekly Red Belt for defense",
            form.cleaned_data["defender"],
        ),
    )
    for award_name, roster in awards:
        pt_models.Accolade.objects.create(
            player=roster.player,
            annual_roster=roster,
            award_date=award_date,
            name=award_name,
            award_org="Talking Hoosier Baseball",
        )
