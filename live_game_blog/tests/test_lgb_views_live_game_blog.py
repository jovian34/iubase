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
def test_live_single_game_blog_page_renders(client, games, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    assert "Joey" in str(response.content)
    assert "Indiana at Kentucky," in str(response.content)
    assert "(FINAL)" in str(response.content)
    assert "Kentucky moves on to Super Regionals" in str(response.content)
    assert "stats" in str(response.content)
    assert "roster" in str(response.content)


@pytest.mark.django_db
def test_live_single_game_blog_page_shows_exhibition(client, games, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_gm_fall.pk]))
    assert response.status_code == 200
    assert "FALL EXHIBITION" in str(response.content)
    assert "stats" not in str(response.content)
    assert "roster" not in str(response.content)


@pytest.mark.django_db
def test_edit_live_single_game_blog_page_renders(
    client, games, scoreboards, entries, logged_user_schwarbs
):
    response = client.get(reverse("edit_live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    assert "Kentucky moves on to Super Regionals" in str(response.content)


@pytest.mark.django_db
def test_edit_live_single_game_blog_page_redirects_not_logged_in(
    client, games, scoreboards, entries
):
    response = client.get(reverse("edit_live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_live_single_game_blog_page_asks_for_password_not_logged_in(
    client, games, scoreboards, entries
):
    response = client.get(reverse("edit_live_game_blog", args=[games.iu_uk_mon.pk]), follow=True)
    assert response.status_code == 200
    assert "Password:" in str(response.content)