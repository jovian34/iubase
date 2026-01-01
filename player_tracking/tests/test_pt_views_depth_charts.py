import pytest
from django.urls import reverse
from datetime import date

from live_game_blog.tests.fixtures.teams import teams
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.annual_rosters import annual_rosters


this_year = date.today().year


@pytest.mark.django_db
def test_spring_depth_chart_renders_indiana_players(
    client, players, teams, annual_rosters
):
    response = client.get(reverse("spring_depth_chart", args=[f"{this_year - 1}"]))
    assert response.status_code == 200
    assert "Catcher" in str(response.context)
    assert f"Spring {this_year - 1} Available Depth Chart" in response.content.decode()
    assert "Devin Taylor" in response.content.decode()
    assert "Nick" not in response.content.decode()  # on different team


@pytest.mark.django_db
def test_spring_depth_chart_shows_no_roster_without_rosters(
    client,
    players,
    teams,
):
    response = client.get(reverse("spring_depth_chart", args=[f"{this_year - 1}"]))
    assert response.status_code == 200
    assert f"Spring {this_year - 1} Roster not yet announced" in response.content.decode()
    assert "Devin Taylor" not in response.content.decode()
