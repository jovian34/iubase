import pytest

from django import urls
from django.template.defaultfilters import floatformat

from live_game_blog.tests.fixtures.games import games
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from live_game_blog.tests.fixtures.home_stadium import home_stadium
from live_game_blog.tests.fixtures.scoreboards import scoreboards
from live_game_blog.tests.fixtures.teams import teams

from accounts.tests.fixtures import user_not_logged_in

from live_game_blog import models as lgb_models
from live_game_blog.logic import weather_daily, weather_hourly


@pytest.mark.django_db
def test_get_weather_for_game_over_one_week_and_render(
    client,
    games, 
    stadiums, 
    stadium_configs, 
    home_stadium,
    scoreboards,
    user_not_logged_in
):
    weather_daily.get_and_set_weather_data_daily()
    fut_games = lgb_models.Game.objects.get(pk=games.iu_uk_far_future.pk)
    assert fut_games.home_team.team_name == "Indiana"
    assert fut_games.first_pitch_temp > -30
    assert fut_games.first_pitch_temp < 120
    assert fut_games.first_pitch_wind_speed
    assert fut_games.first_pitch_wind_angle
    assert "rain" in fut_games.first_pitch_weather_describe
    response = client.get(urls.reverse("live_game_blog", args=[games.iu_uk_far_future.pk]))
    assert "rain" in response.content.decode()
    temp = floatformat(fut_games.first_pitch_temp, 0)
    expected = f"{temp}&deg; F"
    assert expected in response.content.decode()


@pytest.mark.django_db
def test_get_weather_for_game_between_two_days_and_one_week_and_render(
    client,
    games, 
    stadiums, 
    stadium_configs, 
    home_stadium,
    scoreboards,
    user_not_logged_in
):
    weather_daily.get_and_set_weather_data_daily()
    fut_games = lgb_models.Game.objects.get(pk=games.iu_mo.pk)
    assert fut_games.home_team.team_name == "Indiana"
    assert fut_games.first_pitch_temp > -30
    assert fut_games.first_pitch_temp < 120
    assert fut_games.first_pitch_wind_speed
    assert fut_games.first_pitch_wind_angle
    assert fut_games.first_pitch_weather_describe
    assert fut_games.first_pitch_wind_gusts
    assert fut_games.first_pitch_feels_like
    if fut_games.gameday_sunset.hour < 12:
        sunset = fut_games.gameday_sunset.hour + 24
    else:
        sunset = fut_games.gameday_sunset.hour
    assert sunset > 21
    assert sunset < 27
    response = client.get(urls.reverse("live_game_blog", args=[games.iu_mo.pk]))
    temp = floatformat(fut_games.first_pitch_temp, 0)
    expected = f"{temp}&deg; F"
    assert expected in response.content.decode()


@pytest.mark.django_db
def test_get_weather_for_game_between_now_and_two_days_and_render(
    client,
    games, 
    stadiums, 
    stadium_configs, 
    home_stadium,
    scoreboards,
    user_not_logged_in
):
    weather_hourly.get_and_set_weather_data_hourly()
    fut_games = lgb_models.Game.objects.get(pk=games.iu_coastal_tom.pk)
    assert fut_games.home_team.team_name == "Coastal Carolina"
    assert fut_games.first_pitch_temp > -30
    assert fut_games.first_pitch_temp < 120
    assert fut_games.first_pitch_wind_speed
    assert fut_games.first_pitch_wind_angle
    assert fut_games.first_pitch_weather_describe
    assert fut_games.first_pitch_wind_gusts
    assert fut_games.first_pitch_feels_like
    response = client.get(urls.reverse("live_game_blog", args=[games.iu_coastal_tom.pk]))
    temp = floatformat(fut_games.first_pitch_temp, 0)
    expected = f"{temp}&deg; F"
    assert expected in response.content.decode()
