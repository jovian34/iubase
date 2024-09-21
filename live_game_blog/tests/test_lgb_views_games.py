import pytest

from django.urls import reverse

from live_game_blog.tests.fixtures.games import (
    games,
    logged_user_schwarbs,
    user_not_logged_in,
    user_iubase17,
)
from live_game_blog.tests.fixtures.teams import teams
from live_game_blog.tests.fixtures.blog import entries
from live_game_blog.tests.fixtures.scoreboards import scoreboards


@pytest.mark.django_db
def test_games_list_page_renders_road_future(client, teams, games, scoreboards):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    expected = "Indiana at Coastal".replace(" ", "")
    actual = str(response.content).replace(" ", "").replace("\\n", "")
    assert expected in actual


@pytest.mark.django_db
def test_games_list_page_renders_neutral_future(client, teams, games):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "versus" in str(response.content)


@pytest.mark.django_db
def test_games_list_page_does_not_render_canc_games(client, teams, games, scoreboards):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "Coastal Carolina" in str(response.content)
    assert "Miami" not in str(response.content)


@pytest.mark.django_db
def test_games_list_page_does_not_render_past_games(client, teams, games, scoreboards):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "Coastal Carolina" in str(response.content)
    assert "Kentucky" not in str(response.content)


@pytest.mark.django_db
def test_games_list_shows_fall_exhibition(
    client, teams, games, scoreboards
):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "George Mason" in str(response.content)
    assert "FALL EXHIBITION" in str(response.content)


@pytest.mark.django_db
def test_games_list_page_does_not_render_four_games_out(
    client, teams, games, scoreboards
):
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
def test_past_game_renders_partial_with_score(client, teams, games, scoreboards):
    response = client.get(reverse("past_games"))
    assert response.status_code == 200
    assert "Kentucky-4" in str(response.content)