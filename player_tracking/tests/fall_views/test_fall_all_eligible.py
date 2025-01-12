import pytest
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.mlb_draft_date import typical_mlb_draft_date
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.models import Player, MLBDraftDate
from player_tracking.views import set_player_properties
from live_game_blog.tests.fixtures.teams import teams
from player_tracking.views.fall import fall_landing

this_year = date.today().year


@pytest.mark.django_db
def test_all_eligible_players_includes_only_committs_four_years_out(
    client, players, transactions
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("all_eligible_players_fall", args=[f"{this_year + 4}"]), 
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 200
    assert "Owen ten Oever" in str(response.content)
    assert "Xavier Carrera" in str(response.content)
    assert "Andrew Wiggins" not in str(response.content)


@pytest.mark.django_db
def test_all_eligible_players_future_includes_blanket_MLB_draft_caveat(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("all_eligible_players_fall", args=[f"{this_year + 4}"]), 
        HTTP_HX_REQUEST="true",
    )
    assert "as this does not take into account the MLB Draft." in str(response.content)


@pytest.mark.django_db
def test_all_eligible_players_this_year_includes_blanket_MLB_draft_caveat(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("all_eligible_players_fall", args=[f"{this_year}"]), 
        HTTP_HX_REQUEST="true",
    )
    assert "with the exception of players expected to go professional in the MLB Draft." in str(response.content)


@pytest.mark.django_db
def test_all_eligible_players_fall_renders(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("all_eligible_players_fall", args=[f"{this_year + 1}"]), 
        HTTP_HX_REQUEST="true",
    )
    assert "Grant Hollister" in str(response.content)
    assert "Jack Moffitt" not in str(response.content)


@pytest.mark.django_db
def test_all_eligible_players_not_from_HTMX_redirects_to_fall_players(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("all_eligible_players_fall", args=[f"{this_year + 1}"]),
    )
    assert response.status_code == 302
    response = client.get(
        reverse("all_eligible_players_fall", args=[f"{this_year + 1}"]),
        follow=True,
    )
    assert response.status_code == 200
    assert "<title>Players for Fall Seasons by Year</title>" in str(response.content)
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year + 1}/" hx-trigger="load"' in str(response.content)


@pytest.mark.django_db
def test_all_eligible_players_includes_buttons_that_point_HTMX_to_prior_and_next_year(
    client, players, transactions, typical_mlb_draft_date
):
    errors = set_player_properties.set_player_props_get_errors()
    assert len(errors) == 0
    response = client.get(reverse("all_eligible_players_fall", args=[f"{this_year + 1}"]), HTTP_HX_REQUEST="true")
    assert response.status_code == 200
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year}/"' in str(response.content)
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year + 2}/"' in str(response.content)