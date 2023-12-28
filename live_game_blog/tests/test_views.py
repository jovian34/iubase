import pytest
from django.urls import reverse

from live_game_blog.tests.fixtures import teams, games, scoreboard, user_1, blog_entries

@pytest.mark.django_db
def test_games_list_page_renders_road_and_neutral_future(client, teams, games):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "Indiana" in str(response.content)
    assert "versus" in str(response.content)
    assert "at" in str(response.content)

@pytest.mark.django_db
def test_games_list_page_does_not_render_past_games(client, teams, games, scoreboard):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "Coastal Carolina" in str(response.content)
    assert "Kentucky" not in str(response.content)

@pytest.mark.django_db
def test_games_list_page_does_not_render_four_games_out(client, teams, games, scoreboard):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "George Mason" in str(response.content)
    assert "Miami" not in str(response.content)

@pytest.mark.django_db
def test_games_list_page_renders_logo(client, teams, games):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert f"cdn.d1baseball" in str(response.content)

@pytest.mark.django_db
def test_past_game_renders_partial_with_score(client, teams, games, scoreboard):
    response = client.get(reverse("past_games"))
    assert response.status_code == 200
    assert "Kentucky-4" in str(response.content)

@pytest.mark.django_db
def test_live_single_game_blog_page_renders(client, games, scoreboard, blog_entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    assert "Kentucky-4" in str(response.content)
    assert "Indiana-2" in str(response.content)
    assert "(FINAL)" in str(response.content)
    assert "Kentucky moves on to Super Regionals" in str(response.content)
