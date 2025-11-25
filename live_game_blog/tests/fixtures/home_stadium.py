import pytest

from collections import namedtuple
from datetime import date

from live_game_blog import models as lgb_models
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from live_game_blog.tests.fixtures.teams import teams


@pytest.fixture
def home_stadium(client, stadium_configs, teams):
    bart_2013 = lgb_models.HomeStadium.objects.create(
        team=teams.indiana,
        stadium_config=stadium_configs.bart_2013,
        designate_date=date(2013,3,1),        
    )
    home_stad_list = [
        "bart_2013",
    ]
    HomeStadiumObj = namedtuple("HomeStadiumObj", home_stad_list)
    return HomeStadiumObj(
        bart_2013=bart_2013,
    )