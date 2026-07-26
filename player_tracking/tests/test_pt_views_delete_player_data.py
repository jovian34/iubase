import re

import pytest
from bs4 import BeautifulSoup
from django.contrib.auth.models import Permission
from django.urls import reverse

from accounts.tests.fixtures import logged_user_schwarbs
from live_game_blog.tests.fixtures.teams import teams
from player_tracking.models import Accolade, AnnualRoster, SummerAssign, Transaction
from player_tracking.tests.fixtures.accolades import accolades
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.summer import (
    summer_assign,
    summer_leagues,
    summer_teams,
)
from player_tracking.tests.fixtures.transactions import transactions


DELETE_PERMISSIONS = (
    ("delete_annualroster", "delete-roster-"),
    ("delete_transaction", "delete-transaction-"),
    ("delete_summerassign", "delete-summer-assignment-"),
    ("delete_accolade", "delete-accolade-"),
)


def grant_player_tracking_permissions(user, *permission_codenames):
    permissions = Permission.objects.filter(
        content_type__app_label="player_tracking",
        codename__in=permission_codenames,
    )
    user.user_permissions.add(*permissions)


def get_player_page(client, player):
    response = client.get(reverse("single_player_page", args=[player.pk]))
    return BeautifulSoup(response.content, "html.parser")


def find_rendered_delete_controls(page, control_prefix):
    controls = page.find_all(id=re.compile(f"^{control_prefix}"))
    return [control for control in controls if control.find("button")]


def assert_delete_button(page, control_id, delete_url, section_id):
    delete_control = page.find(id=control_id)
    assert delete_control is not None
    delete_button = delete_control.find("button")
    assert delete_button.get_text(strip=True) == "🗑️"
    assert delete_button["aria-label"] == "Delete"
    assert "delete-button" in delete_button["class"]
    assert delete_button["hx-delete"] == delete_url
    assert delete_button["hx-target"] == f"#{section_id}"
    assert delete_button.has_attr("hx-confirm")
    assert "X-CSRFToken" in delete_button["hx-headers"]
    return delete_control


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("permission_codename", "visible_control_prefix"),
    DELETE_PERMISSIONS,
)
def test_player_page_renders_only_delete_buttons_allowed_by_permission(
    client,
    players,
    annual_rosters,
    transactions,
    summer_assign,
    accolades,
    logged_user_schwarbs,
    permission_codename,
    visible_control_prefix,
):
    grant_player_tracking_permissions(logged_user_schwarbs, permission_codename)

    page = get_player_page(client, players.devin_taylor)

    visible_controls = find_rendered_delete_controls(page, visible_control_prefix)
    assert visible_controls
    for _, other_control_prefix in DELETE_PERMISSIONS:
        if other_control_prefix != visible_control_prefix:
            assert not find_rendered_delete_controls(page, other_control_prefix)


@pytest.mark.django_db
def test_delete_buttons_render_for_every_player_record_with_confirmation(
    client,
    players,
    annual_rosters,
    transactions,
    summer_assign,
    accolades,
    logged_user_schwarbs,
):
    grant_player_tracking_permissions(
        logged_user_schwarbs,
        *(permission for permission, _ in DELETE_PERMISSIONS),
        "change_annualroster",
        "change_transaction",
        "change_summerassign",
    )
    page = get_player_page(client, players.devin_taylor)

    for roster in (annual_rosters.dt_soph, annual_rosters.dt_fresh):
        delete_control = assert_delete_button(
            page,
            f"delete-roster-{roster.pk}-control",
            reverse("delete_roster_year", args=[roster.pk]),
            "annual-rosters",
        )
        assert delete_control.parent.find(id=f"edit-roster-{roster.pk}-control")

    player_transactions = (
        transactions.dt_draft_ranked,
        transactions.dt_nli,
        transactions.dt_verbal,
    )
    for transaction in player_transactions:
        delete_control = assert_delete_button(
            page,
            f"delete-transaction-{transaction.pk}-control",
            reverse("delete_transaction", args=[transaction.pk]),
            "transactions",
        )
        assert delete_control.parent.find(
            id=f"edit-transaction-{transaction.pk}-control"
        )

    for assignment in (summer_assign.dt_usa_ty, summer_assign.dt_kg_ly):
        delete_control = assert_delete_button(
            page,
            f"delete-summer-assignment-{assignment.pk}-control",
            reverse("delete_summer_assignment", args=[assignment.pk]),
            "summer-ball",
        )
        assert delete_control.parent.find(
            id=f"edit-summer-assignment-{assignment.pk}-control"
        )

    player_accolades = (
        accolades.dt_ly_ps_aa_second_team,
        accolades.dt_ly_aa_second_team,
        accolades.dt_ly_b1g_first_team,
    )
    for accolade in player_accolades:
        assert_delete_button(
            page,
            f"delete-accolade-{accolade.pk}-control",
            reverse("delete_accolade", args=[accolade.pk]),
            "annual-rosters",
        )


@pytest.mark.django_db
def test_delete_actions_forbidden_without_permissions(
    client,
    annual_rosters,
    transactions,
    summer_assign,
    accolades,
    logged_user_schwarbs,
):
    delete_requests = (
        (
            "delete_roster_year",
            annual_rosters.dt_fresh,
            AnnualRoster,
        ),
        (
            "delete_transaction",
            transactions.dt_verbal,
            Transaction,
        ),
        (
            "delete_summer_assignment",
            summer_assign.dt_usa_ty,
            SummerAssign,
        ),
        (
            "delete_accolade",
            accolades.dt_ly_b1g_first_team,
            Accolade,
        ),
    )

    for view_name, record, model in delete_requests:
        response = client.delete(reverse(view_name, args=[record.pk]))
        assert response.status_code == 403
        assert model.objects.filter(pk=record.pk).exists()


@pytest.mark.django_db
def test_delete_actions_reject_get_requests(
    client,
    annual_rosters,
    transactions,
    summer_assign,
    accolades,
    logged_user_schwarbs,
):
    grant_player_tracking_permissions(
        logged_user_schwarbs,
        *(permission for permission, _ in DELETE_PERMISSIONS),
    )
    delete_requests = (
        ("delete_roster_year", annual_rosters.dt_fresh, AnnualRoster),
        ("delete_transaction", transactions.dt_verbal, Transaction),
        ("delete_summer_assignment", summer_assign.dt_usa_ty, SummerAssign),
        ("delete_accolade", accolades.dt_ly_b1g_first_team, Accolade),
    )

    for view_name, record, model in delete_requests:
        response = client.get(reverse(view_name, args=[record.pk]))
        assert response.status_code == 405
        assert model.objects.filter(pk=record.pk).exists()


@pytest.mark.django_db
def test_authorized_delete_actions_remove_data_and_render_updated_sections(
    client,
    annual_rosters,
    transactions,
    summer_assign,
    accolades,
    logged_user_schwarbs,
):
    grant_player_tracking_permissions(
        logged_user_schwarbs,
        *(permission for permission, _ in DELETE_PERMISSIONS),
    )
    delete_requests = (
        (
            "delete_roster_year",
            annual_rosters.dt_fresh,
            AnnualRoster,
            "annual-rosters",
        ),
        (
            "delete_transaction",
            transactions.dt_verbal,
            Transaction,
            "transactions",
        ),
        (
            "delete_summer_assignment",
            summer_assign.dt_usa_ty,
            SummerAssign,
            "summer-ball",
        ),
        (
            "delete_accolade",
            accolades.dt_ly_b1g_first_team,
            Accolade,
            "annual-rosters",
        ),
    )

    for view_name, record, model, section_id in delete_requests:
        response = client.delete(
            reverse(view_name, args=[record.pk]),
            HTTP_HX_REQUEST="true",
        )
        assert response.status_code == 200
        assert not model.objects.filter(pk=record.pk).exists()
        assert f'id="{section_id}"' in response.content.decode()


@pytest.mark.django_db
def test_deleting_accolades_renders_their_owning_sections(
    client,
    players,
    annual_rosters,
    summer_assign,
    accolades,
    logged_user_schwarbs,
):
    grant_player_tracking_permissions(
        logged_user_schwarbs,
        "delete_accolade",
    )
    standalone_accolade = Accolade.objects.create(
        player=players.devin_taylor,
        name="National Player of the Week",
        award_org="National Organization",
    )
    delete_requests = (
        (accolades.rk_northwoods_pitch_of_year, "summer-ball"),
        (standalone_accolade, "other-accolades"),
    )

    for accolade, section_id in delete_requests:
        response = client.delete(
            reverse("delete_accolade", args=[accolade.pk]),
            HTTP_HX_REQUEST="true",
        )

        assert response.status_code == 200
        assert not Accolade.objects.filter(pk=accolade.pk).exists()
        assert f'id="{section_id}"' in response.content.decode()
