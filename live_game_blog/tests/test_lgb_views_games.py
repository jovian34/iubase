import pytest

from django.urls import reverse

from live_game_blog.tests.fixtures.games import games
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from accounts.tests.fixtures import (
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
    expected = "Indiana <em>@</em> Coastal".replace(" ", "")
    actual = str(response.content).replace(" ", "").replace("\\n", "")
    assert expected in actual


@pytest.mark.django_db
def test_games_list_page_renders_neutral_future(client, teams, games):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "vs." in str(response.content)


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
def test_games_list_page_renders_add_game_if_staff(
    admin_client, teams, games, scoreboards
):
    response = admin_client.get(reverse("games"))
    assert response.status_code == 200
    assert "Add game" in str(response.content)


@pytest.mark.django_db
def test_games_list_page_no_add_game_if_user_has_no_perms(
    client, logged_user_schwarbs, teams, games, scoreboards
):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "Add game" not in str(response.content)


@pytest.mark.django_db
def test_games_list_shows_event(client, teams, games, scoreboards):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "George Mason" in str(response.content)
    assert "Fall exhibition" in str(response.content)


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
def test_past_game_renders_partial_with_weekday(client, teams, games, scoreboards):
    response = client.get(
        reverse("past_games"),
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 200
    assert "Wed, Oct. 4, 2023," in str(response.content)


@pytest.mark.django_db
def test_past_game_renders_partial_with_seed_and_score(
    client, teams, games, scoreboards
):
    response = client.get(
        reverse("past_games"),
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == 200
    assert "Kentucky Wildcats (1-seed): 4" in str(response.content)
    assert "Wed, Oct. 4, 2023," in str(response.content)


@pytest.mark.django_db
def test_past_game_partial_redirects_to_games_when_not_requested_by_HTMX(
    client, teams, games, scoreboards
):
    response = client.get(reverse("past_games"))
    assert response.status_code == 302
    response = client.get(
        reverse("past_games"),
        follow=True,
    )
    assert response.status_code == 200
    expected = "Indiana<em>@</em>Coastal".replace(" ", "")
    actual = str(response.content).replace(" ", "").replace("\\n", "")
    assert expected in actual
    assert "Kentucky-4" not in str(response.content)
