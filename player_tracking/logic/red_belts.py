from django.db import transaction
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from player_tracking import models as pt_models
from player_tracking import choices


@transaction.atomic
def save_weekly_red_belts(form):
    award_date = form.cleaned_data["award_date"]
    citation = form.cleaned_data["citation"]
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
            citation=citation,
            name=award_name,
            award_org="Talking Hoosier Baseball",
        )


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


def require_add_accolade_permission(request):
    if not request.user.has_perm("player_tracking.add_accolade"):
        raise PermissionDenied