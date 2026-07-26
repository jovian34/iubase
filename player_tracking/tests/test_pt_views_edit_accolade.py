from datetime import date

import pytest
from bs4 import BeautifulSoup
from django.contrib.auth.models import Permission
from django.urls import reverse

from accounts.tests.fixtures import logged_user_schwarbs
from live_game_blog.tests.fixtures.teams import teams
from player_tracking.models import Accolade
from player_tracking.tests.fixtures.accolades import accolades
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.summer import (
    summer_assign,
    summer_leagues,
    summer_teams,
)


this_year = date.today().year


def grant_accolade_permissions(user, *permission_codenames):
    permissions = Permission.objects.filter(
        content_type__app_label="player_tracking",
        codename__in=permission_codenames,
    )
    user.user_permissions.add(*permissions)


def get_player_page(client, player):
    response = client.get(reverse("single_player_page", args=[player.pk]))
    return BeautifulSoup(response.content, "html.parser")


def edited_accolade_data(roster):
    return {
        "name": "Updated All-Conference Award",
        "award_date": date(this_year, 6, 1),
        "award_org": "Updated Organization",
        "description": "Updated accolade details.",
        "citation": "https://example.com/updated-accolade",
        "annual_roster": roster.pk,
        "summer_assign": [],
    }


def assert_edit_accolade_button(page, accolade):
    control_id = f"edit-accolade-{accolade.pk}-control"
    edit_control = page.find(id=control_id)
    assert edit_control is not None
    edit_button = edit_control.find("button", string="✏️")
    assert edit_button is not None
    assert "edit-button" in edit_button["class"]
    assert edit_button["aria-label"] == "Edit"
    assert edit_button["title"] == "Edit accolade"
    assert edit_button["hx-get"] == reverse("edit_accolade", args=[accolade.pk])
    assert edit_button["hx-target"] == f"#{control_id}"

    action_group = edit_control.parent
    assert action_group.find(id=f"delete-accolade-{accolade.pk}-control")
    accolade_record = action_group.find_parent("li")
    record_elements = list(accolade_record.descendants)
    assert record_elements.index(accolade_record.find("p")) < record_elements.index(
        action_group
    )


@pytest.mark.django_db
def test_player_page_omits_accolade_edit_buttons_without_permission(
    client,
    players,
    annual_rosters,
    accolades,
    logged_user_schwarbs,
):
    page = get_player_page(client, players.devin_taylor)

    edit_controls = page.find_all(
        id=lambda value: value and value.startswith("edit-accolade-")
    )
    assert not edit_controls


@pytest.mark.django_db
def test_player_page_renders_edit_button_for_every_accolade_with_permission(
    client,
    players,
    annual_rosters,
    summer_assign,
    accolades,
    logged_user_schwarbs,
):
    grant_accolade_permissions(
        logged_user_schwarbs,
        "change_accolade",
        "delete_accolade",
    )
    other_accolade = Accolade.objects.create(
        player=players.devin_taylor,
        award_date=date(this_year, 1, 15),
        name="Standalone Award",
        award_org="Independent Organization",
    )

    devin_page = get_player_page(client, players.devin_taylor)
    devin_accolades = (
        accolades.dt_ly_ps_aa_second_team,
        accolades.dt_ly_aa_second_team,
        accolades.dt_ly_b1g_first_team,
        other_accolade,
    )
    for accolade in devin_accolades:
        assert_edit_accolade_button(devin_page, accolade)

    ryan_page = get_player_page(client, players.ryan_kraft)
    assert_edit_accolade_button(ryan_page, accolades.rk_northwoods_pitch_of_year)


@pytest.mark.django_db
def test_edit_accolade_form_forbidden_without_permission(
    client,
    accolades,
    logged_user_schwarbs,
):
    response = client.get(
        reverse(
            "edit_accolade",
            args=[accolades.dt_ly_b1g_first_team.pk],
        )
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_accolade_form_renders_current_values_for_authorized_user(
    client,
    accolades,
    logged_user_schwarbs,
):
    grant_accolade_permissions(logged_user_schwarbs, "change_accolade")
    accolade = accolades.dt_ly_b1g_first_team
    form_url = reverse("edit_accolade", args=[accolade.pk])

    response = client.get(form_url, HTTP_HX_REQUEST="true")
    form = response.context["form"]
    rendered_form = BeautifulSoup(response.content, "html.parser").find("form")

    assert response.status_code == 200
    assert form.initial["name"] == accolade.name
    assert form.initial["award_date"] == accolade.award_date
    assert form.initial["award_org"] == accolade.award_org
    assert form.initial["description"] == accolade.description
    assert form.initial["citation"] == accolade.citation
    assert form.initial["annual_roster"] == accolade.annual_roster
    assert form.initial["summer_assign"] == accolade.summer_assign
    assert rendered_form["hx-post"] == form_url
    assert rendered_form["hx-target"] == "#annual-rosters"


@pytest.mark.django_db
def test_edit_accolade_submission_forbidden_without_permission(
    client,
    annual_rosters,
    accolades,
    logged_user_schwarbs,
):
    accolade = accolades.dt_ly_b1g_first_team
    original_name = accolade.name

    response = client.post(
        reverse("edit_accolade", args=[accolade.pk]),
        edited_accolade_data(annual_rosters.dt_soph),
        HTTP_HX_REQUEST="true",
    )
    accolade.refresh_from_db()

    assert response.status_code == 403
    assert accolade.name == original_name


@pytest.mark.django_db
def test_authorized_edit_accolade_updates_and_renders_owning_section(
    client,
    annual_rosters,
    accolades,
    logged_user_schwarbs,
):
    grant_accolade_permissions(logged_user_schwarbs, "change_accolade")
    accolade = accolades.dt_ly_b1g_first_team

    response = client.post(
        reverse("edit_accolade", args=[accolade.pk]),
        edited_accolade_data(annual_rosters.dt_soph),
        HTTP_HX_REQUEST="true",
    )
    updated_accolade = Accolade.objects.get(pk=accolade.pk)
    output = response.content.decode()

    assert response.status_code == 200
    assert updated_accolade.name == "Updated All-Conference Award"
    assert updated_accolade.award_date == date(this_year, 6, 1)
    assert updated_accolade.award_org == "Updated Organization"
    assert updated_accolade.description == "Updated accolade details."
    assert updated_accolade.citation == "https://example.com/updated-accolade"
    assert updated_accolade.annual_roster == annual_rosters.dt_soph
    assert updated_accolade.summer_assign is None
    assert 'id="annual-rosters"' in output
    assert "Updated All-Conference Award" in output
    assert 'title="Edit accolade"' in output
