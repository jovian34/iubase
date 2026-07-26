from django.contrib.auth import decorators as auth
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from player_tracking.models import Accolade, AnnualRoster, SummerAssign, Transaction
from player_tracking.views import set_player_properties, single_player_page


@auth.login_required
@require_http_methods(["DELETE"])
def delete_roster_year(request, roster_id):
    require_permission(request, "player_tracking.delete_annualroster")
    roster = get_object_or_404(AnnualRoster, pk=roster_id)
    player_id = roster.player_id
    roster.delete()
    set_player_properties.set_player_props_get_errors()
    return render_player_section(
        request,
        player_id,
        "player_tracking/partials/annual_rosters.html",
    )


@auth.login_required
@require_http_methods(["DELETE"])
def delete_transaction(request, transaction_id):
    require_permission(request, "player_tracking.delete_transaction")
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    player_id = transaction.player_id
    transaction.delete()
    set_player_properties.set_player_props_get_errors()
    return render_player_section(
        request,
        player_id,
        "player_tracking/partials/player_transactions.html",
    )


@auth.login_required
@require_http_methods(["DELETE"])
def delete_summer_assignment(request, assignment_id):
    require_permission(request, "player_tracking.delete_summerassign")
    assignment = get_object_or_404(SummerAssign, pk=assignment_id)
    player_id = assignment.player_id
    assignment.delete()
    return render_player_section(
        request,
        player_id,
        "player_tracking/partials/player_summer_ball.html",
    )


@auth.login_required
@require_http_methods(["DELETE"])
def delete_accolade(request, accolade_id):
    require_permission(request, "player_tracking.delete_accolade")
    accolade = get_object_or_404(Accolade, pk=accolade_id)
    player_id = accolade.player_id
    template_name = get_accolade_section_template(accolade)
    accolade.delete()
    return render_player_section(request, player_id, template_name)


def require_permission(request, permission_name):
    if not request.user.has_perm(permission_name):
        raise PermissionDenied


def get_accolade_section_template(accolade):
    if accolade.annual_roster_id:
        return "player_tracking/partials/annual_rosters.html"
    if accolade.summer_assign_id:
        return "player_tracking/partials/player_summer_ball.html"
    return "player_tracking/partials/other_accolades.html"


def render_player_section(request, player_id, template_name):
    return single_player_page.render_player_section(
        request,
        player_id,
        template_name,
    )
