import os
import math
from datetime import timedelta, datetime

from django.utils import timezone
import requests

from live_game_blog import models as lgb_models
from live_game_blog.logic import location, wind


def get_and_set_weather_data_daily():
    seven_days_from_now = timezone.now() + timedelta(days=7)
    forty_seven_hours_from_now = timezone.now() + timedelta(hours=47)
    api_key = os.environ.get("WEATHER_API_KEY")
    get_weather_and_set_data_for_games_more_than_one_week_out(
        seven_days_from_now, api_key
    )

    games_two_to_seven_days_out = lgb_models.Game.objects.filter(
        first_pitch__gt=forty_seven_hours_from_now,
        first_pitch__lte=seven_days_from_now,
    )
    for game in games_two_to_seven_days_out:
        lat, long = location.get_lat_and_long_of_stadium(game)
        api_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={long}&exclude=current,minutely,alerts&appid={api_key}&units=imperial"
        data_dict = get_weather_data_dict(api_url)
        delta = game.first_pitch - timezone.now()
        days_out = int(math.floor(delta.total_seconds() / 86400))
        game.first_pitch_temp = data_dict["daily"][days_out]["temp"]["day"]
        game.first_pitch_feels_like = data_dict["daily"][days_out]["feels_like"]["day"]
        game.first_pitch_wind_speed = data_dict["daily"][days_out]["wind_speed"]
        game.first_pitch_wind_angle = wind.convert_wind_direction_to_opposite(data_dict["daily"][days_out]["wind_deg"])
        game.first_pitch_wind_gusts = data_dict["daily"][days_out]["wind_gust"]
        game.first_pitch_weather_describe = data_dict["daily"][days_out]["summary"]
        game.gameday_sunset = datetime.fromtimestamp(
            data_dict["daily"][days_out]["sunset"], tz=timezone.UTC
        )
        print(game.gameday_sunset)
        game.save()


def get_weather_and_set_data_for_games_more_than_one_week_out(
    seven_days_from_now, api_key
):
    five_hundred_days_from_now = timezone.now() + timedelta(days=500)
    games_seven_days_out = lgb_models.Game.objects.filter(
        first_pitch__gt=seven_days_from_now,
        first_pitch__lte=five_hundred_days_from_now,
    )
    for game in games_seven_days_out:
        lat, long = location.get_lat_and_long_of_stadium(game)
        data_dict = get_weather_data_more_than_one_week_out(game, lat, long, api_key)
        save_weather_data_more_than_one_week_out(game, data_dict)


def get_weather_data_more_than_one_week_out(game, lat, long, api_key):
    first_pitch = game.first_pitch.strftime("%Y-%m-%d")
    api_url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={long}&date={first_pitch}&units=imperial&appid={api_key}"
    return get_weather_data_dict(api_url)


def get_weather_data_dict(api_url):
    r = requests.get(api_url)
    return r.json()


def save_weather_data_more_than_one_week_out(game, data_dict):
    edit_game = lgb_models.Game.objects.get(pk=game.pk)
    edit_game.first_pitch_temp = data_dict["temperature"]["afternoon"]
    edit_game.first_pitch_wind_speed = data_dict["wind"]["max"]["speed"]
    edit_game.first_pitch_wind_angle = wind.convert_wind_direction_to_opposite(data_dict["wind"]["max"]["direction"])
    make_description_from_predicted_rain(data_dict, edit_game)
    print(edit_game)
    edit_game.save()


def make_description_from_predicted_rain(data_dict, edit_game):
    rain = float(data_dict["precipitation"]["total"])  # in mm
    if rain > 50:
        edit_game.first_pitch_weather_describe = "heavy rain"
    elif rain > 25:
        edit_game.first_pitch_weather_describe = "moderate rain"
    elif rain > 0:
        edit_game.first_pitch_weather_describe = "light rain"
    else:
        edit_game.first_pitch_weather_describe = "no rain"
