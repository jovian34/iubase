import os
from datetime import timedelta

from django.utils import timezone
import requests

from live_game_blog import models as lgb_models


def get_and_set_weather_data_daily():
    seven_days_from_now = timezone.now() + timedelta(days=7)
    five_hundred_days_from_now = timezone.now() + timedelta(days=500)
    forty_seven_hours_from_now = timezone.now() + timedelta(hours=47)
    get_weather_and_set_data_for_games_more_than_one_week_out(seven_days_from_now, five_hundred_days_from_now)



def get_weather_and_set_data_for_games_more_than_one_week_out(seven_days_from_now, five_hundred_days_from_now):
    games_seven_days_out = lgb_models.Game.objects.filter(
        first_pitch__gt=seven_days_from_now,
        first_pitch__lte=five_hundred_days_from_now,
    )
    for game in games_seven_days_out:
        lat, long = get_lat_and_long_of_stadium(game)        
        data_dict = get_weather_data_more_than_one_week_out(game, lat, long)
        save_weather_data_more_than_one_week_out(game, data_dict)
    

def get_weather_data_more_than_one_week_out(game, lat, long):
    first_pitch = game.first_pitch.strftime("%Y-%m-%d")
    api_key = os.environ.get("WEATHER_API_KEY")
    api_url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={long}&date={first_pitch}&units=imperial&appid={api_key}"
    r = requests.get(api_url)
    data_dict = r.json()
    return data_dict


def save_weather_data_more_than_one_week_out(game, data_dict):
    edit_game = lgb_models.Game.objects.get(pk=game.pk)
    edit_game.first_pitch_temp = data_dict["temperature"]["afternoon"]
    edit_game.first_pitch_wind_speed = data_dict["wind"]["max"]["speed"]
    edit_game.first_pitch_wind_angle = data_dict["wind"]["max"]["direction"]
    make_description_from_predicted_rain(data_dict, edit_game)
    edit_game.save()
        

def get_lat_and_long_of_stadium(game):
    if game.neutral_site:
        lat = game.stadium_config.stadium.lat
        long = game.stadium_config.stadium.long
    else:
        home_stadiums = lgb_models.HomeStadium.objects.filter(team=game.home_team.pk).order_by("-designate_date")
        for home_stadium in home_stadiums:
            if game.first_pitch.date() > home_stadium.designate_date:
                lat = home_stadium.stadium_config.stadium.lat
                long = home_stadium.stadium_config.stadium.long
                break
        else:
            raise ValueError(f"No home stadium set for {game.home_team.team_name} for the date of first pitch")
    return lat,long


def make_description_from_predicted_rain(data_dict, edit_game):
    rain = float(data_dict["precipitation"]["total"]) # in mm
    if rain > 50:
        edit_game.first_pitch_weather_describe = "heavy rain"
    elif rain > 25:
        edit_game.first_pitch_weather_describe = "moderate rain"
    elif rain > 0:
        edit_game.first_pitch_weather_describe = "light rain"
    else:
        edit_game.first_pitch_weather_describe = "no rain"


