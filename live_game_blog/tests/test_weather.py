import pytest

from live_game_blog.tests.fixtures.games import games
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from live_game_blog.tests.fixtures.home_stadium import home_stadium
from live_game_blog.tests.fixtures.teams import teams

from live_game_blog import models as lgb_models
from live_game_blog import weather


@pytest.mark.django_db
def test_get_weather_for_game_over_one_week(
    games, 
    stadiums, 
    stadium_configs, 
    home_stadium
):
    weather.get_weather_for_games_over_one_week_from_now()
    fut_games = lgb_models.Game.objects.get(pk=games.iu_uk_far_future.pk)
    assert fut_games.home_team.team_name == "Indiana"
    assert fut_games.first_pitch_temp
    assert fut_games.first_pitch_wind_speed
    assert fut_games.first_pitch_wind_angle
    assert "rain" in fut_games.first_pitch_weather_describe



