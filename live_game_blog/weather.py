import os
from datetime import timedelta

from django.utils import timezone
import requests

from live_game_blog import models as lgb_models



def get_weather_for_games_over_one_week_from_now():
    seven_days_from_now = timezone.now() + timedelta(days=7)
    five_hund_days_from_now = timezone.now() + timedelta(days=500)
    games_seven_days_out = lgb_models.Game.objects.filter(
        first_pitch__gt=seven_days_from_now,
        first_pitch__lte=five_hund_days_from_now,
    )
    for game in games_seven_days_out:
        if game.neutral_site:
            lat = game.stadium.lat
            long = game.stadium.long
        else:
            home_stadiums = lgb_models.HomeStadium.objects.filter(team=game.home_team.pk).order_by("-designate_date")
            for home_stadium in home_stadiums:
                if game.first_pitch.date() > home_stadium.designate_date:
                    lat = home_stadium.stadium_config.stadium.lat
                    long = home_stadium.stadium_config.stadium.long
                    break
            else:
                raise ValueError(f"No home stadium set for {game.home_team.team_name} for the date of first pitch")
        
        first_pitch = game.first_pitch.strftime("%Y-%m-%d")
        api_key = os.environ.get("WEATHER_API_KEY")
        api_url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={long}&date={first_pitch}&units=imperial&appid={api_key}"
        r = requests.get(api_url)
        data_dict = r.json()
        print(data_dict)
        edit_game = lgb_models.Game.objects.get(pk=game.pk)
        edit_game.first_pitch_temp = data_dict["temperature"]["afternoon"]
        edit_game.first_pitch_wind_speed = data_dict["wind"]["max"]["speed"]
        edit_game.first_pitch_wind_angle = data_dict["wind"]["max"]["direction"]
        make_description_from_predicted_rain(data_dict, edit_game)
        edit_game.save()


def make_description_from_predicted_rain(data_dict, edit_game):
    rain = float(data_dict["precipitation"]["total"])
    if rain > 2:
        edit_game.first_pitch_weather_describe = "heavy rain"
    elif rain > 1:
        edit_game.first_pitch_weather_describe = "moderate rain"
    elif rain > 0:
        edit_game.first_pitch_weather_describe = "light rain"
    else:
        edit_game.first_pitch_weather_describe = "no rain"


def get_wind_description(cf, blowing):
    cf_offset = angle_difference(cf, blowing)
    if abs(cf_offset) <= 15:
        return "blowing out to centerfield"
    elif 15 < cf_offset <= 35:
        return "blowing out to left-centerfield"
    elif -15 > cf_offset >= -35:
        return "blowing out to right-centerfield"
    elif 35 < cf_offset <= 55:
        return "blowing out to left field"
    elif -35 > cf_offset >= -55:
        return "blowing out to right field"
    elif abs(cf_offset) >= 165:
        return "blowing in from centerfield"
    elif 165 > cf_offset >= 145:
        return "blowing in from right-centerfield"
    elif -165 < cf_offset <= -145:
        return "blowing in from left-centerfield"
    elif 145 > cf_offset >= 125:
        return "blowing in from right field"
    elif -145 < cf_offset <= -125:
        return "blowing in from left field"        
    elif 55 < cf_offset < 125:
        return "cross wind from right to left"
    elif -55 > cf_offset > -125:
        return "cross wind from left to right"
    else:
        raise ValueError
    
    
def angle_difference(angle_cf, angle_wind):
    # Calculate the initial difference
    difference = angle_cf - angle_wind

    # Normalize the difference to be within the range of 0 to 360 degrees
    normalized_difference = (difference + 360) % 360

    # Determine the direction, make negative for clock
    if normalized_difference > 180:
        angle_diff = -(360 - normalized_difference)
    else:
        angle_diff = normalized_difference

    return angle_diff