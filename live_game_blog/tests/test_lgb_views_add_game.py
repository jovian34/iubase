import pytest

from django.urls import reverse

from live_game_blog.tests.fixtures.games import (
    games,
    logged_user_schwarbs,
    user_not_logged_in,
    user_iubase17,
)
from live_game_blog.tests.fixtures.teams import teams
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from live_game_blog.tests.fixtures.home_stadium import home_stadium
from live_game_blog.tests.fixtures.scoreboards import scoreboards
from live_game_blog.tests.fixtures.form_data import forms
from conference.tests.fixtures.conferences import conferences

from live_game_blog import models as lgb_models

from conference.logic import year


@pytest.mark.django_db
def test_add_game_page_renders_template(admin_client,):
    response = admin_client.get(reverse("add_game"))
    assert response.status_code == 200
    assert "Game at Neutral Site" in response.content.decode()
    assert "Away team D1Baseball.com national ranking" in response.content.decode()
    assert "Away team national tournament seed" in response.content.decode()
    assert "Home team tournament seed" in response.content.decode()
    assert "Live Stats Link" in response.content.decode()
    assert "Video Stream or TV provider" in response.content.decode()
    assert "Student Audio Link" in response.content.decode()
    assert "Date and Time of First Pitch YYYY-MM-DD-HHMM in ET military time" in str(
        response.content
    )
    assert "Primary Audio Link" in response.content.decode()


@pytest.mark.django_db
def test_add_game_get_shows_forbidden_without_perms(client, logged_user_schwarbs):
    response = client.get(reverse("add_game"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_neutral_game(admin_client, teams, stadiums, stadium_configs, games, scoreboards, forms):
    response = admin_client.post(
        reverse("add_neutral_game"),
        forms.iu_v_gm,
        follow=True,
    )
    assert response.status_code == 200
    assert f"Feb. 14, {year.get_spring_year()}, 6:30 p.m. first pitch" in response.content.decode()
    assert "Scoreboard: George Mason-0, Indiana-0 | Top Inning: 1" in str(response.context)


@pytest.mark.django_db
def test_add_neutral_game_post_shows_forbidden_without_perms(client, logged_user_schwarbs, teams, games, scoreboards, forms):
    response = client.post(
        reverse("add_neutral_game"),
        forms.iu_v_gm,
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_tourney_game(
    admin_client, teams, games, forms, scoreboards, stadiums, stadium_configs, home_stadium
):
    response = admin_client.post(
        reverse("add_game"),
        forms.uk_tourney,
        follow=True,
    )
    assert response.status_code == 200
    assert "Indiana (3-seed)" in response.content.decode()
    assert "at" in response.content.decode()
    assert "no. 20" in response.content.decode()
    assert "Kentucky (1-seed)" in response.content.decode()
    assert "(#14 National Seed)" in response.content.decode()


@pytest.mark.django_db
def test_add_tourney_game_saves_present_stadium_config(
    admin_client, teams, games, forms, scoreboards, stadiums, stadium_configs, home_stadium
):
    response = admin_client.post(
        reverse("add_game"),
        forms.uk_tourney,
        follow=True,
    )
    assert response.status_code == 200
    game = lgb_models.Game.objects.get(live_stats="https://stats.statbroadcast.com/broadcast/?id=491945&vislive=ind")
    assert game.stadium_config.stadium_name == "Kentucky Proud Park"


@pytest.mark.django_db
def test_add_future_tourney_game_saves_stadium_config(
    admin_client, teams, games, forms, scoreboards, stadiums, stadium_configs, home_stadium
):
    response = admin_client.post(
        reverse("add_game"),
        forms.uk_tourney_future,
        follow=True,
    )
    assert response.status_code == 200
    game = lgb_models.Game.objects.get(live_stats="https://stats.statbroadcast.com/broadcast/?id=8975433245&vislive=ind")
    assert game.stadium_config.stadium_name == "Kentucky Very Proud Park"


@pytest.mark.django_db
def test_add_road_game_without_stadium(
    admin_client, teams, games, forms, scoreboards, stadiums, stadium_configs, home_stadium
):
    response = admin_client.post(
        reverse("add_game"),
        forms.gm_hosts_iu,
        follow=True,
    )
    assert response.status_code == 200
    assert "Errors from Add Game" in response.content.decode()
    assert "George Mason has no home stadium configuration to apply." in response.content.decode()


@pytest.mark.django_db
def test_add_game_post_asks_for_login_when_not_logged_in(client, forms, teams):
    response = client.post(
        reverse("add_game"),
        forms.uk_tourney,
        follow=True,
    )
    assert response.status_code == 200
    assert "Sign In Via Google" in response.content.decode()
