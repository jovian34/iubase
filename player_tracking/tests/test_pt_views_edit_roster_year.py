import pytest
from bs4 import BeautifulSoup
from django.contrib.auth.models import Permission
from django.urls import reverse

from accounts.tests.fixtures import logged_user_schwarbs
from live_game_blog.tests.fixtures.teams import teams
from player_tracking.models import AnnualRoster
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.players import players


def grant_change_annual_roster_permission(user):
    permission = Permission.objects.get(
        content_type__app_label="player_tracking",
        codename="change_annualroster",
    )
    user.user_permissions.add(permission)


def edited_roster_data(roster, team):
    return {
        "spring_year": roster.spring_year,
        "team": team.pk,
        "jersey": 42,
        "status": "Spring Roster",
        "primary_position": "First Base",
        "secondary_position": "Corner Outfield",
    }


@pytest.mark.django_db
def test_player_page_omits_roster_edit_buttons_without_permission(
    client,
    players,
    annual_rosters,
    logged_user_schwarbs,
):
    response = client.get(
        reverse("single_player_page", args=[players.devin_taylor.pk])
    )
    page = BeautifulSoup(response.content, "html.parser")

    for roster in (annual_rosters.dt_soph, annual_rosters.dt_fresh):
        heading = page.find(id=f"roster-{roster.pk}-heading")
        assert heading is not None
        assert heading.find(class_="record-actions") is None


@pytest.mark.django_db
def test_player_page_renders_edit_button_for_each_roster_with_permission(
    client,
    players,
    annual_rosters,
    logged_user_schwarbs,
):
    grant_change_annual_roster_permission(logged_user_schwarbs)

    response = client.get(
        reverse("single_player_page", args=[players.devin_taylor.pk])
    )
    annual_rosters_section = BeautifulSoup(
        response.content,
        "html.parser",
    ).find(id="annual-rosters")

    for roster in (annual_rosters.dt_soph, annual_rosters.dt_fresh):
        heading = annual_rosters_section.find(id=f"roster-{roster.pk}-heading")
        assert heading is not None
        control_id = f"edit-roster-{roster.pk}-control"
        edit_control = heading.find(id=control_id)
        assert edit_control is not None
        edit_button = edit_control.find("button", string="✏️")
        assert edit_button is not None
        assert edit_button["aria-label"] == "Edit"
        assert edit_button["title"] == "Edit roster year"
        assert edit_button["hx-get"] == reverse("edit_roster_year", args=[roster.pk])
        assert edit_button["hx-target"] == f"#{control_id}"


@pytest.mark.django_db
def test_edit_roster_form_forbidden_without_permission(
    client,
    annual_rosters,
    logged_user_schwarbs,
):
    response = client.get(
        reverse("edit_roster_year", args=[annual_rosters.dt_soph.pk])
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_roster_form_renders_current_values_for_authorized_user(
    client,
    annual_rosters,
    logged_user_schwarbs,
):
    grant_change_annual_roster_permission(logged_user_schwarbs)
    roster = annual_rosters.dt_soph
    form_url = reverse("edit_roster_year", args=[roster.pk])

    response = client.get(form_url, HTTP_HX_REQUEST="true")
    form = response.context["form"]
    rendered_form = BeautifulSoup(response.content, "html.parser").find("form")

    assert response.status_code == 200
    assert form.initial["spring_year"] == roster.spring_year
    assert form.initial["team"] == roster.team
    assert form.initial["jersey"] == roster.jersey
    assert form.initial["status"] == roster.status
    assert form.initial["primary_position"] == roster.primary_position
    assert form.initial["secondary_position"] == roster.secondary_position
    assert rendered_form["hx-post"] == form_url
    assert rendered_form["hx-target"] == "#annual-rosters"


@pytest.mark.django_db
def test_edit_roster_submission_forbidden_without_permission(
    client,
    annual_rosters,
    teams,
    logged_user_schwarbs,
):
    roster = annual_rosters.dt_soph
    original_team = roster.team

    response = client.post(
        reverse("edit_roster_year", args=[roster.pk]),
        edited_roster_data(roster, teams.duke),
        HTTP_HX_REQUEST="true",
    )
    roster.refresh_from_db()

    assert response.status_code == 403
    assert roster.team == original_team
    assert roster.jersey != 42


@pytest.mark.django_db
def test_non_htmx_roster_edit_is_rejected_without_update(
    client,
    annual_rosters,
    teams,
    logged_user_schwarbs,
):
    grant_change_annual_roster_permission(logged_user_schwarbs)
    roster = annual_rosters.dt_soph
    original_team = roster.team
    original_jersey = roster.jersey
    edit_url = reverse("edit_roster_year", args=[roster.pk])

    get_response = client.get(edit_url)
    post_response = client.post(
        edit_url,
        edited_roster_data(roster, teams.duke),
    )
    roster.refresh_from_db()

    assert get_response.status_code == 400
    assert post_response.status_code == 400
    assert roster.team == original_team
    assert roster.jersey == original_jersey


@pytest.mark.django_db
def test_authorized_edit_roster_submission_updates_and_renders_roster_section(
    client,
    annual_rosters,
    teams,
    logged_user_schwarbs,
):
    grant_change_annual_roster_permission(logged_user_schwarbs)
    roster = annual_rosters.dt_soph

    response = client.post(
        reverse("edit_roster_year", args=[roster.pk]),
        edited_roster_data(roster, teams.duke),
        HTTP_HX_REQUEST="true",
    )
    updated_roster = AnnualRoster.objects.get(pk=roster.pk)
    output = response.content.decode()

    assert response.status_code == 200
    assert updated_roster.team == teams.duke
    assert updated_roster.jersey == 42
    assert updated_roster.status == "Spring Roster"
    assert updated_roster.primary_position == "First Base"
    assert updated_roster.secondary_position == "Corner Outfield"
    assert 'id="annual-rosters"' in output
    assert f"{updated_roster.spring_year} Duke" in output
    assert 'aria-label="Edit"' in output
    assert "✏️</button>" in output
