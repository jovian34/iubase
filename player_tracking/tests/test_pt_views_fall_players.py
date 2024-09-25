import pytest
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.mlb_draft_date import typical_mlb_draft_date
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.models import Player, MLBDraftDate
from player_tracking.views import fall_players
from live_game_blog.tests.fixtures.teams import teams
from accounts.tests.fixtures import logged_user_schwarbs

this_year = date.today().year


@pytest.mark.django_db
def test_fall_players_main_page_renders(
    client, players, transactions, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("fall_players"))
    assert "Players for Fall Seasons by Year" in str(response.content)


@pytest.mark.django_db
def test_all_eligible_players_includes_only_committs_four_years_out(
    client, players, transactions, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(
        reverse("all_eligible_players_fall", args=[f"{this_year + 4}"])
    )
    assert response.status_code == 200
    assert "Owen ten Oever" in str(response.content)
    assert "Xavier Carrera" in str(response.content)
    assert "Andrew Wiggins" not in str(response.content)


@pytest.mark.django_db
def test_projected_players_renders_current_players(
    client, players, transactions, typical_mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall_depth", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert f"Projected Players For Fall {this_year}" in str(response.content)
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_fall_players_renders_projected_players_for_current_year(
    client, players, transactions, typical_mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall_depth", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert f"Projected Players For Fall {this_year}" in str(response.content)
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_projected_players_excludes_transfer_portal_entrants(
    client, players, transactions, typical_mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall_depth", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert "Brooks Ey" not in str(response.content)


@pytest.mark.django_db
def test_projected_players_includes_incoming_high_school_commit(
    client, players, transactions, typical_mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall_depth", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert "Grant Hollister" in str(response.content)


@pytest.mark.django_db
def test_projected_players_excludes_future_high_school_commit(
    client, players, transactions, typical_mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall_depth", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert "Xavier" not in str(response.content)


@pytest.mark.django_db
def test_projected_players_includes_transfer_commit(
    client, players, transactions, typical_mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall_depth", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert "Holton Compton" in str(response.content)


@pytest.mark.django_db
def test_all_eligible_players_fall_renders(
    client, players, transactions, typical_mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    response = client.get(
        reverse("all_eligible_players_fall", args=[f"{this_year + 1}"])
    )
    assert "Grant Hollister" in str(response.content)
    assert "Jack Moffitt" not in str(response.content)


@pytest.mark.django_db
def test_fall_players_points_HTMX_to_current_year_without_year_specified(
    client, players, transactions, typical_mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("fall_players"))
    assert response.status_code == 200
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year}/"' in str(response.content)


@pytest.mark.django_db
def test_fall_roster_includes_buttons_that_point_HTMX_to_prior_and_next_year(
    client, players, transactions, typical_mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("fall_roster", args=[f"{this_year - 1}"]))
    assert response.status_code == 200
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year}/"' in str(response.content)
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year - 2}/"' in str(response.content)


@pytest.mark.django_db
def test_fall_projection_includes_buttons_that_point_HTMX_to_prior_and_next_year(
    client, players, transactions, typical_mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall_depth", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year + 1}/"' in str(response.content)
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year - 1}/"' in str(response.content)


@pytest.mark.django_db
def test_all_eligible_players_includes_buttons_that_point_HTMX_to_prior_and_next_year(
    client, players, transactions, typical_mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("all_eligible_players_fall", args=[f"{this_year + 1}"]))
    assert response.status_code == 200
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year}/"' in str(response.content)
    assert f'hx-get="/player_tracking/fall_players_redirect/{this_year + 2}/"' in str(response.content)


