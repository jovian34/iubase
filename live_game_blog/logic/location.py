from live_game_blog import models as lgb_models


def get_lat_and_long_of_stadium(game):
    if game.neutral_site:
        lat = game.stadium_config.stadium.lat
        long = game.stadium_config.stadium.long
    else:
        home_stadiums = lgb_models.HomeStadium.objects.filter(
            team=game.home_team.pk
        ).order_by("-designate_date")
        for home_stadium in home_stadiums:
            if game.first_pitch.date() > home_stadium.designate_date:
                lat = home_stadium.stadium_config.stadium.lat
                long = home_stadium.stadium_config.stadium.long
                break
        else:
            raise ValueError(
                f"No home stadium set for {game.home_team.team_name} for the date of first pitch"
            )
    return lat, long
