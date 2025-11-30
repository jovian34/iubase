import pytest
from django import urls

from live_game_blog.tests.fixtures.teams import teams
from live_game_blog.tests.fixtures.home_stadium import home_stadium
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from live_game_blog.tests.fixtures.stadiums import stadiums

def test_stadium_page_renders(client):
    response = client.get(urls.reverse("stadiums"))
    assert response.status_code == 200
    assert "Stadium Actions" in str(response.content)
    assert "get teams without stadium configuration"


@pytest.mark.django_db
def test_teams_wo_stad_config_partial_renders_correct_teams(client, teams, home_stadium, stadium_configs, stadiums):
    response = client.get(urls.reverse("teams_wo_stad_config"))
    assert response.status_code == 200
    assert "Kentucky" in str(response.content)
    assert "Indiana" not in str(response.content)
    assert "Add Stadium Data" in str(response.content)