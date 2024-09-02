import pytest
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.mlb_draft_date import mlb_draft_date
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.tests.fixtures.summer import (
    summer_assign,
    summer_leagues,
    summer_teams,
)
from live_game_blog.tests.fixtures import teams


this_year = date.today().year


@pytest.mark.django_db
def test_single_player_page_renders_one_player_only(client, annual_rosters):
    response = client.get(
        reverse(
            "single_player_page",
            args=[annual_rosters.dt_fresh.player.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)
    assert "Nick" not in str(response.content)


@pytest.mark.django_db
def test_single_player_page_renders_summer_teams(
    client, annual_rosters, summer_assign, summer_leagues, summer_teams
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[annual_rosters.dt_fresh.player.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)
    assert "Summer Ball:" in str(response.content)
    assert (
        f"{this_year}: USA Collegiate National Team of the International Friendship League"
        in str(response.content)
    )