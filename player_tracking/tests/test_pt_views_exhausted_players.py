import pytest
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.mlb_draft_date import typical_mlb_draft_date
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from live_game_blog.tests.fixtures.teams import teams

from player_tracking.views import set_player_properties


this_year = date.today().year

def test_manual_url_exhausted_player_is_correct():
    manual = f"/player_tracking/exhausted_players/{this_year}/"
    reversed = reverse("exhausted_players", args=[f"{this_year}"])
    assert manual == reversed    


@pytest.mark.django_db
def test_exhausted_players_page_renders(
    client,
    players,
    annual_rosters,
    typical_mlb_draft_date,
    prof_orgs,
    transactions,
    teams,
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(reverse("exhausted_players", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert f"All players ending eligibilty after Spring {this_year}"


@pytest.mark.django_db
def test_exhausted_players_page_shows_senior_for_his_last_season(
    client,
    players,
    annual_rosters,
    typical_mlb_draft_date,
    prof_orgs,
    transactions,
    teams,
):
    set_player_properties.set_player_props_get_errors()
    response = client.get(reverse("exhausted_players", args=[f"{this_year + 1}"]))
    assert "Cole Gilley" in str(response.content)
