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
from live_game_blog import weather


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
    weather.get_weather_for_games_over_one_week_from_now()
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


testdata = [
    (45, 41, "blowing out to centerfield"),
    (0, 355, "blowing out to centerfield"),
    (90, 99, "blowing out to centerfield"),
    (135, 127, "blowing out to centerfield"),
    (180, 190, "blowing out to centerfield"),
    (270, 259, "blowing out to centerfield"),
    (320, 333, "blowing out to centerfield"),
    (45, 20, "blowing out to left-centerfield"),
    (90, 70, "blowing out to left-centerfield"),
    (135, 115, "blowing out to left-centerfield"),
    (180, 160, "blowing out to left-centerfield"),
    (270, 250, "blowing out to left-centerfield"),
    (345, 327, "blowing out to left-centerfield"),
    (45, 65, "blowing out to right-centerfield"),
    (45, 81, "blowing out to right field"),
    (45, 99, "blowing out to right field"),
    (45, 9, "blowing out to left field"),
    (45, 351, "blowing out to left field"),
    (270, 290, "blowing out to right-centerfield"),
    (359, 26, "blowing out to right-centerfield"),
]


@pytest.mark.parametrize("cf,blowing,expected", testdata)
def test_get_wind_direction(cf, blowing, expected):
    assert weather.get_wind_description(cf, blowing) == expected