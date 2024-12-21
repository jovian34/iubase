import pytest
from django.urls import reverse
from datetime import date

from player_tracking.views import set_player_properties

from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.tests.fixtures.mlb_draft_date import typical_mlb_draft_date
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from live_game_blog.tests.fixtures.teams import teams

this_year = date.today().year


@pytest.mark.django_db
def test_landing_page_renders(
    client, players, transactions
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(reverse("fall_players"))
    assert "Players for Fall Seasons by Year" in str(response.content)


@pytest.mark.django_db
def test_prior_year_redirect_redirects_to_fall_roster(
    client, players, transactions, typical_mlb_draft_date, annual_rosters,
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("fall_players_redirect", args=[f"{this_year - 1}"]),
    )
    assert response.status_code == 302
    assert "fall_roster" in str(response['Location'])


@pytest.mark.django_db
def test_future_year_redirect_redirects_to_all_eligible(
    client, players, transactions, typical_mlb_draft_date, annual_rosters,
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("fall_players_redirect", args=[f"{this_year + 1}"]),
    )
    assert response.status_code == 302
    assert "all_eligible_players_fall" in str(response['Location'])


@pytest.mark.django_db
def test_this_year_redirect_redirects_to_projected_players_fall_depth(
    client, players, transactions, typical_mlb_draft_date, annual_rosters,
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("fall_players_redirect", args=[f"{this_year}"]),
    )
    assert response.status_code == 302
    assert "projected_players_fall_depth" in str(response['Location'])


@pytest.mark.django_db
def test_this_year_no_draft_date_redirect_redirects_to_all_eligible(
    client, players, transactions, annual_rosters,
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("fall_players_redirect", args=[f"{this_year}"]),
    )
    assert response.status_code == 302
    assert "all_eligible_players_fall" in str(response['Location'])


@pytest.mark.django_db
def test_fall_players_renders_projected_players_for_current_year(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("projected_players_fall_depth", args=[f"{this_year}"]), 
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 200
    assert f"Projected Players For Fall {this_year}" in str(response.content)
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_fall_players_points_HTMX_to_current_year_without_year_specified(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(reverse("fall_players"))
    assert response.status_code == 200
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year}/"' in str(response.content)


@pytest.mark.django_db
def test_fall_roster_includes_buttons_that_point_HTMX_to_prior_and_next_year(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("fall_roster", args=[f"{this_year - 1}"]), 
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 200
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year}/"' in str(response.content)
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year - 2}/"' in str(response.content)