import pytest
from django import urls

from player_tracking.tests.fixtures.accolades import accolades
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.summer import (
    summer_assign,
    summer_leagues,
    summer_teams,
)
from player_tracking.tests.fixtures.annual_rosters import annual_rosters

from live_game_blog.tests.fixtures.teams import teams


@pytest.mark.django_db
def test_accolade_page_renders(client):
    response = client.get(urls.reverse("accolades"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_accolade_page_shows_accolade(
    client, accolades, players, annual_rosters, teams
):
    response = client.get(urls.reverse("accolades"))
    assert "Pre-season second team All-American Outfielder" in response.content.decode()


@pytest.mark.django_db
def test_accolade_page_shows_college_team_if_not_indiana(
    client, accolades, players, annual_rosters, teams
):
    response = client.get(urls.reverse("accolades"))
    assert "College Team: Miami" in response.content.decode()
    assert "College Team: Indiana" not in response.content.decode()
