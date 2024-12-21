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
def test_projected_players_renders_current_players(
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
def test_projected_players_excludes_transfer_portal_entrants(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("projected_players_fall_depth", args=[f"{this_year}"]), 
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 200
    assert "Brooks Ey" not in str(response.content)


@pytest.mark.django_db
def test_projected_players_includes_incoming_high_school_commit(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("projected_players_fall_depth", args=[f"{this_year}"]), 
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 200
    assert "Grant Hollister" in str(response.content)


@pytest.mark.django_db
def test_projected_players_excludes_future_high_school_commit(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("projected_players_fall_depth", args=[f"{this_year}"]), 
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 200
    assert "Xavier" not in str(response.content)


@pytest.mark.django_db
def test_projected_players_includes_transfer_commit(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("projected_players_fall_depth", args=[f"{this_year}"]), 
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 200
    assert "Holton Compton" in str(response.content)


@pytest.mark.django_db
def test_projected_players_depth_lists_pitcher_before_infielder(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("projected_players_fall_depth", args=[f"{this_year}"]), 
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 200
    output = str(response.content)
    shortstop = output.find("Holton Compton")
    pitcher = output.find("Grant Hollister")
    assert shortstop > pitcher


@pytest.mark.django_db
def test_projected_players_alpha_lists_alphabetical_order_by_last_name(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("projected_players_fall_alpha", args=[f"{this_year}"]), 
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 200
    output = str(response.content)
    compton = output.find("Holton Compton")
    hollister = output.find("Grant Hollister")
    assert hollister > compton


@pytest.mark.django_db
def test_projected_players_not_from_HTMX_redirects_to_fall_players(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("projected_players_fall_depth", args=[f"{this_year}"]),
    )
    assert response.status_code == 302
    response = client.get(
        reverse("projected_players_fall_depth", args=[f"{this_year}"]),
        follow=True,
    )
    assert response.status_code == 200
    assert "<title>Players for Fall Seasons by Year</title>" in str(response.content)
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year}/" hx-trigger="load"' in str(response.content)


@pytest.mark.django_db
def test_fall_projection_includes_buttons_that_point_HTMX_to_prior_and_next_year(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("projected_players_fall_depth", args=[f"{this_year}"]), 
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 200
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year + 1}/"' in str(response.content)
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year - 1}/"' in str(response.content)


@pytest.mark.django_db
def test_fall_projection_not_called_by_HTMX_redirects_to_fall_players(
    client, players, transactions, typical_mlb_draft_date
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(
        reverse("projected_players_fall_depth", args=[f"{this_year}"]),
    )
    assert response.status_code == 302
    response = client.get(
        reverse("projected_players_fall_depth", args=[f"{this_year}"]),
        follow=True,
    )
    assert response.status_code == 200
    assert "<title>Players for Fall Seasons by Year</title>" in str(response.content)
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year}/" hx-trigger="load"' in str(response.content)