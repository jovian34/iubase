from datetime import date

import pytest
from bs4 import BeautifulSoup
from django.contrib.auth.models import Permission
from django.urls import reverse

from accounts.tests.fixtures import logged_user_schwarbs
from player_tracking.models import SummerAssign
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.summer import (
    summer_assign,
    summer_leagues,
    summer_teams,
)


this_year = date.today().year


def grant_change_summer_assignment_permission(user):
    permission = Permission.objects.get(
        content_type__app_label="player_tracking",
        codename="change_summerassign",
    )
    user.user_permissions.add(permission)


def edited_summer_assignment_data(summer_league, summer_team):
    return {
        "summer_year": this_year - 2,
        "summer_league": summer_league.pk,
        "summer_team": summer_team.pk,
        "source": "Updated summer assignment source",
        "citation": "https://example.com/updated-summer-assignment",
    }


@pytest.mark.django_db
def test_player_page_omits_summer_assignment_edit_buttons_without_permission(
    client,
    players,
    summer_assign,
    logged_user_schwarbs,
):
    response = client.get(
        reverse("single_player_page", args=[players.devin_taylor.pk])
    )

    assert "edit summer assignment</button>" not in response.content.decode()


@pytest.mark.django_db
def test_player_page_renders_edit_button_after_each_summer_assignment(
    client,
    players,
    summer_assign,
    logged_user_schwarbs,
):
    grant_change_summer_assignment_permission(logged_user_schwarbs)
    response = client.get(
        reverse("single_player_page", args=[players.devin_taylor.pk])
    )
    summer_ball_section = BeautifulSoup(
        response.content,
        "html.parser",
    ).find(id="summer-ball")

    for assignment in (summer_assign.dt_usa_ty, summer_assign.dt_kg_ly):
        control_id = f"edit-summer-assignment-{assignment.pk}-control"
        edit_control = summer_ball_section.find(id=control_id)
        assert edit_control is not None
        edit_button = edit_control.find("button", string="edit summer assignment")
        assert edit_button is not None
        assert edit_button["hx-get"] == reverse(
            "edit_summer_assignment",
            args=[assignment.pk],
        )
        assert edit_button["hx-target"] == f"#{control_id}"

        assignment_record = edit_control.find_parent("li")
        assignment_elements = list(assignment_record.descendants)
        assignment_details = assignment_record.find("p")
        details_position = assignment_elements.index(assignment_details)
        control_position = assignment_elements.index(edit_control)
        assert details_position < control_position


@pytest.mark.django_db
def test_edit_summer_assignment_form_forbidden_without_permission(
    client,
    summer_assign,
    logged_user_schwarbs,
):
    response = client.get(
        reverse(
            "edit_summer_assignment",
            args=[summer_assign.dt_usa_ty.pk],
        )
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_summer_assignment_form_renders_current_values_when_authorized(
    client,
    summer_assign,
    logged_user_schwarbs,
):
    grant_change_summer_assignment_permission(logged_user_schwarbs)
    assignment = summer_assign.dt_usa_ty
    form_url = reverse("edit_summer_assignment", args=[assignment.pk])

    response = client.get(form_url, HTTP_HX_REQUEST="true")
    form = response.context["form"]
    rendered_form = BeautifulSoup(response.content, "html.parser").find("form")

    assert response.status_code == 200
    assert form.initial["summer_year"] == assignment.summer_year
    assert form.initial["summer_league"] == assignment.summer_league
    assert form.initial["summer_team"] == assignment.summer_team
    assert form.initial["source"] == assignment.source
    assert form.initial["citation"] == assignment.citation
    assert rendered_form["hx-post"] == form_url
    assert rendered_form["hx-target"] == "#summer-ball"


@pytest.mark.django_db
def test_edit_summer_assignment_submission_forbidden_without_permission(
    client,
    summer_assign,
    summer_leagues,
    summer_teams,
    logged_user_schwarbs,
):
    assignment = summer_assign.dt_usa_ty
    original_team = assignment.summer_team

    response = client.post(
        reverse("edit_summer_assignment", args=[assignment.pk]),
        edited_summer_assignment_data(summer_leagues.nw, summer_teams.gb),
        HTTP_HX_REQUEST="true",
    )
    assignment.refresh_from_db()

    assert response.status_code == 403
    assert assignment.summer_team == original_team
    assert assignment.source is None


@pytest.mark.django_db
def test_authorized_edit_summer_assignment_updates_and_renders_summer_section(
    client,
    summer_assign,
    summer_leagues,
    summer_teams,
    logged_user_schwarbs,
):
    grant_change_summer_assignment_permission(logged_user_schwarbs)
    assignment = summer_assign.dt_usa_ty

    response = client.post(
        reverse("edit_summer_assignment", args=[assignment.pk]),
        edited_summer_assignment_data(summer_leagues.nw, summer_teams.gb),
        HTTP_HX_REQUEST="true",
    )
    updated_assignment = SummerAssign.objects.get(pk=assignment.pk)
    output = response.content.decode()

    assert response.status_code == 200
    assert updated_assignment.summer_year == this_year - 2
    assert updated_assignment.summer_league == summer_leagues.nw
    assert updated_assignment.summer_team == summer_teams.gb
    assert updated_assignment.source == "Updated summer assignment source"
    assert (
        updated_assignment.citation
        == "https://example.com/updated-summer-assignment"
    )
    assert 'id="summer-ball"' in output
    assert "Green Bay" in output
    assert "edit summer assignment</button>" in output
