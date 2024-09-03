import pytest

from django.urls import reverse

from live_game_blog.tests.fixtures.games import (
    games,
    logged_user_schwarbs,
    user_not_logged_in,
    user_iubase17,
)
from live_game_blog.tests.fixtures.teams import teams
from live_game_blog.tests.fixtures.scoreboards import scoreboards
from live_game_blog.tests.fixtures.form_data import forms


@pytest.mark.django_db
def test_add_game_page_renders_template(client, logged_user_schwarbs):
    response = client.get(reverse("add_game"))
    assert response.status_code == 200
    assert "Is this a neutral site or host is designated away?" in str(response.content)
    assert "Away team D1Baseball.com national ranking" in str(response.content)
    assert "Away team national tournament seed" in str(response.content)
    assert "Home team tournament seed" in str(response.content)
    assert "Live Stats Link" in str(response.content)
    assert "Video Stream or TV provider" in str(response.content)
    assert "Student Audio Link" in str(response.content)
    assert "Date and Time of First Pitch YYYY-MM-DD-HHMM in ET military time" in str(
        response.content
    )
    assert "Primary Audio Link" in str(response.content)


@pytest.mark.django_db
def test_add_game(client, logged_user_schwarbs, teams, games, scoreboards, forms):
    response = client.post(
        reverse("add_game"),
        forms.iu_v_gm,
        follow=True,
    )
    assert response.status_code == 200
    assert "Feb. 14, 2025, 6:30 p.m. first pitch" in str(response.content)
    assert "Scoreboard: George Mason-0, Indiana-0 | Top Inning: 1" in str(
        response.context
    )


@pytest.mark.django_db
def test_add_tourney_game(client, logged_user_schwarbs, teams, games, forms, scoreboards):
    response = client.post(
        reverse("add_game"),
        forms.uk_tourney,
        follow=True,
    )
    assert response.status_code == 200
    assert "Indiana (3-seed)" in str(response.content)
    assert "at" in str(response.content)
    assert "no. 20" in str(response.content)
    assert "Kentucky (1-seed)" in str(response.content)
    assert "(#14 National Seed)" in str(response.content)


@pytest.mark.django_db
def test_add_game_post_asks_for_login_when_not_logged_in(client, teams):
    response = client.post(
        reverse("add_game"),
        {
            "home_team": [str(teams.indiana.pk)],
            "away_team": [str(teams.gm.pk)],
            "neutral_site": ["on"],
            "live_stats": [
                "https://stats.statbroadcast.com/broadcast/?id=491945&vislive=ind"
            ],
            "first_pitch": ["2025-02-14-1830"],
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Password:" in str(response.content)
