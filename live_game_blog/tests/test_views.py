import pytest
from django.urls import reverse

from live_game_blog.tests.fixtures import teams, games, game_status, user_1

@pytest.mark.django_db
def test_games_list_page_renders_road_and_neutral_future(client, teams, games):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "Indiana" in str(response.content)
    assert "versus" in str(response.content)
    assert "at" in str(response.content)

@pytest.mark.django_db
def test_games_list_page_does_not_render_past_games(client, teams, games):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "Coastal Carolina" in str(response.content)
    assert "Kentucky" not in str(response.content)

@pytest.mark.django_db
def test_games_list_page_requests_logo(client, teams, games):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert f"team_logo/{teams.indiana.pk}/" in str(response.content)

@pytest.mark.django_db
def test_team_logo_renders_logo_partial(client, teams, games):
    response = client.get(reverse("team_logo", args=[teams.indiana.pk]))
    assert response.status_code == 200
    assert "indiana.png" in str(response.content)

@pytest.mark.django_db
def test_past_game_renders_partial_with_score(client, teams, games, game_status):
    response = client.get(reverse("past_games"))
    assert response.status_code == 200
    assert f"team_logo/{teams.indiana.pk}/" in str(response.content)
    assert "Kentucky-4" in str(response.content)

@pytest.mark.django_db
def test_view_blog_page_renders(client, teams, games):
    response = client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
