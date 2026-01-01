import pytest
from django import urls

from live_game_blog.tests.fixtures.teams import teams
from live_game_blog.tests.fixtures.home_stadium import home_stadium
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.games import logged_user_schwarbs


@pytest.mark.django_db
def test_stadium_page_fails_wo_perms(client, logged_user_schwarbs):
    response = client.get(urls.reverse("stadiums"))
    assert response.status_code == 403


def test_stadium_page_renders(admin_client):
    response = admin_client.get(urls.reverse("stadiums"))
    assert response.status_code == 200
    assert "Stadium Actions" in response.content.decode()
    assert "get teams without stadium configuration"


@pytest.mark.django_db
def test_teams_wo_stad_config_partial_fails_wo_perms(client, logged_user_schwarbs):
    response = client.get(urls.reverse("teams_wo_stad_config"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_teams_wo_stad_config_partial_renders_correct_teams(admin_client, teams, home_stadium, stadium_configs, stadiums):
    response = admin_client.get(urls.reverse("teams_wo_stad_config"))
    assert response.status_code == 200
    assert "North Carolina" in response.content.decode()
    assert "Indiana" not in response.content.decode()
    assert "Add Stadium Data" in response.content.decode()