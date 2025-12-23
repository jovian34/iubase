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
        api_url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={long}&date={first_pitch}&appid={api_key}"
        r = requests.get(api_url)
        data_dict = r.json()
        print(data_dict)
        edit_game = lgb_models.Game.objects.get(pk=game.pk)
        edit_game.first_pitch_temp = data_dict["temperature"]["afternoon"]
        edit_game.first_pitch_wind_speed = data_dict["wind"]["max"]["speed"]
        edit_game.first_pitch_wind_angle = data_dict["wind"]["max"]["direction"]
        rain = float(data_dict["precipitation"]["total"])
        if rain > 2:
            edit_game.first_pitch_weather_describe = "heavy rain"
        elif rain > 1:
            edit_game.first_pitch_weather_describe = "moderate rain"
        elif rain > 0:
            edit_game.first_pitch_weather_describe = "light rain"
        else:
            edit_game.first_pitch_weather_describe = "no rain"
        edit_game.save()