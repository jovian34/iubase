import pytest

from collections import namedtuple
from datetime import date

from live_game_blog import models as lgb_models
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.teams import teams


@pytest.fixture
def home_stadium(client, stadiums, teams):
    bart_2013 = lgb_models.HomeStadium.objects.create(
        team=teams.indiana,
        stadium=stadiums.bart,
        designate_date=date(2013,3,1),        
    )
    home_stad_list = [
        "bart_2013",
    ]
    HomeStadiumObj = namedtuple("HomeStadiumObj", home_stad_list)
    return HomeStadiumObj(
        bart_2013=bart_2013,
    )