import os
from datetime import timedelta

from django.utils import timezone

from live_game_blog import models as lgb_models
from live_game_blog.logic import location, weather_daily


def get_and_set_weather_data_hourly():
    forty_seven_hours_from_now = timezone.now() + timedelta(hours=47)
    api_key = os.environ.get("WEATHER_API_KEY")

    games_in_next_forty_seven_hours = lgb_models.Game.objects.filter(
        first_pitch__gt=timezone.now(),
        first_pitch__lte=forty_seven_hours_from_now,
    )

    for game in games_in_next_forty_seven_hours:
        lat, long = location.get_lat_and_long_of_stadium(game)
        api_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={long}&exclude=current,minutely,alerts&appid={api_key}&units=imperial"
        data_dict = weather_daily.get_weather_data_dict(api_url)
        delta = game.first_pitch - timezone.now()
        hours_out = int(round(delta.total_seconds() / 3600))
        game.first_pitch_temp = data_dict["hourly"][hours_out]["temp"]
        game.first_pitch_feels_like = data_dict["hourly"][hours_out]["feels_like"]
        game.first_pitch_wind_speed = data_dict["hourly"][hours_out]["wind_speed"]
        game.first_pitch_wind_angle = data_dict["hourly"][hours_out]["wind_deg"]
        game.first_pitch_wind_gusts = data_dict["hourly"][hours_out]["wind_gust"]
        game.first_pitch_weather_describe = data_dict["hourly"][hours_out]["weather"][
            0
        ]["description"]
        game.save()
