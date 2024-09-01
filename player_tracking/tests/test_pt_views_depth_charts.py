import pytest
from django.urls import reverse
from datetime import date

from live_game_blog.tests.fixtures import teams
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.annual_rosters import annual_rosters


this_year = date.today().year


@pytest.mark.django_db
def test_fall_depth_chart_renders(client, players, teams, annual_rosters):
    response = client.get(reverse("fall_depth_chart", args=[f"{this_year - 1}"]))
    assert response.status_code == 200
    assert "Corner Outfield" in str(response.content)
    assert f"Fall {this_year - 1} Available Depth Chart" in str(response.content)
    assert "Devin Taylor" in str(response.content)
    assert "Brayden" not in str(response.content)


@pytest.mark.django_db
def test_spring_depth_chart_renders_indiana_players(
    client, players, teams, annual_rosters
):
    response = client.get(reverse("spring_depth_chart", args=[f"{this_year - 1}"]))
    assert response.status_code == 200
    assert "Catcher" in str(response.context)
    assert f"Spring {this_year - 1} Available Depth Chart" in str(response.content)
    assert "Devin Taylor" in str(response.content)
    assert "Nick" not in str(response.content)  # on different team