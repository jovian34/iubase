import pytest
from datetime import date
from django.urls import reverse

from accounts.tests.fixtures import logged_user_schwarbs
from player_tracking.models import AnnualRoster
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.mlb_draft_date import typical_mlb_draft_date
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.views import set_player_properties
from live_game_blog.tests.fixtures.teams import teams


this_year = date.today().year


@pytest.mark.django_db
def test_enter_fall_roster_redirects_not_logged_in(client):
    response = client.get(reverse("enter_fall_roster", args=[this_year]))

    assert response.status_code == 302


@pytest.mark.django_db
def test_enter_fall_roster_forbidden_without_add_permission(
    client, logged_user_schwarbs
):
    response = client.get(reverse("enter_fall_roster", args=[this_year]))

    assert response.status_code == 403


@pytest.mark.django_db
def test_enter_fall_roster_lists_projected_players_with_default_positions(
    admin_client, players, transactions, typical_mlb_draft_date, annual_rosters
):
    set_player_properties.set_player_props_get_errors()

    response = admin_client.get(reverse("enter_fall_roster", args=[this_year]))
    output = response.content.decode()

    assert response.status_code == 200
    assert "Jake Stadler" in output
    assert 'value="Catcher" selected' in output
    assert "Jersey Number" in output
    assert "Primary Fielding Position" in output


@pytest.mark.django_db
def test_enter_fall_roster_htmx_post_creates_annual_roster(
    admin_client,
    players,
    transactions,
    typical_mlb_draft_date,
    annual_rosters,
    teams,
):
    set_player_properties.set_player_props_get_errors()
    data = {
        "form-TOTAL_FORMS": "1",
        "form-INITIAL_FORMS": "0",
        "form-MIN_NUM_FORMS": "0",
        "form-MAX_NUM_FORMS": "1000",
        "form-0-player": str(players.jake_stadler.pk),
        "form-0-jersey": "9",
        "form-0-primary_position": "Catcher",
    }

    response = admin_client.post(
        reverse("enter_fall_roster", args=[this_year]),
        data,
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert AnnualRoster.objects.filter(
        player=players.jake_stadler,
        spring_year=this_year + 1,
        team=teams.indiana,
        jersey=9,
        primary_position="Catcher",
        status="Fall Roster",
    ).exists()


@pytest.mark.django_db
def test_enter_fall_roster_skips_player_without_jersey_number(
    admin_client, players, transactions, typical_mlb_draft_date, annual_rosters
):
    set_player_properties.set_player_props_get_errors()
    data = {
        "form-TOTAL_FORMS": "1",
        "form-INITIAL_FORMS": "0",
        "form-MIN_NUM_FORMS": "0",
        "form-MAX_NUM_FORMS": "1000",
        "form-0-player": str(players.jake_stadler.pk),
        "form-0-jersey": "",
        "form-0-primary_position": "Catcher",
    }

    response = admin_client.post(
        reverse("enter_fall_roster", args=[this_year]),
        data,
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert not AnnualRoster.objects.filter(
        player=players.jake_stadler,
        spring_year=this_year + 1,
    ).exists()


@pytest.mark.django_db
def test_enter_fall_roster_ignores_stale_submission_for_existing_roster(
    admin_client,
    players,
    transactions,
    typical_mlb_draft_date,
    annual_rosters,
    teams,
):
    AnnualRoster.objects.create(
        player=players.jake_stadler,
        spring_year=this_year + 1,
        team=teams.indiana,
        jersey=9,
        status="Fall Roster",
        primary_position="Catcher",
    )
    set_player_properties.set_player_props_get_errors()
    data = {
        "form-TOTAL_FORMS": "1",
        "form-INITIAL_FORMS": "0",
        "form-MIN_NUM_FORMS": "0",
        "form-MAX_NUM_FORMS": "1000",
        "form-0-player": str(players.jake_stadler.pk),
        "form-0-jersey": "9",
        "form-0-primary_position": "Catcher",
    }

    response = admin_client.post(
        reverse("enter_fall_roster", args=[this_year]),
        data,
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 200
    assert AnnualRoster.objects.filter(
        player=players.jake_stadler,
        spring_year=this_year + 1,
    ).count() == 1


@pytest.mark.django_db
def test_enter_fall_roster_post_forbidden_without_add_permission(
    client,
    logged_user_schwarbs,
    players,
    transactions,
    typical_mlb_draft_date,
    annual_rosters,
):
    response = client.post(
        reverse("enter_fall_roster", args=[this_year]),
        {},
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == 403
