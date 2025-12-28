import pytest

from collections import namedtuple
from datetime import date

from live_game_blog import models as lgb_models
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from live_game_blog.tests.fixtures.teams import teams


@pytest.fixture
def home_stadium(client, stadium_configs, teams):
    bart = lgb_models.HomeStadium.objects.create(
        team=teams.indiana,
        stadium_config=stadium_configs.bart,
        designate_date=date(date.today().year-12,3,1),        
    )
    springs = lgb_models.HomeStadium.objects.create(
        team=teams.coastal,
        stadium_config=stadium_configs.springs,
        designate_date=date(date.today().year-10,2,1),
    )
    banks = lgb_models.HomeStadium.objects.create(
        team=teams.iowa,
        stadium_config=stadium_configs.banks,
        designate_date=date(date.today().year-15,3,1),   
    )
    proud = lgb_models.HomeStadium.objects.create(
        team=teams.kentucky,
        stadium_config=stadium_configs.proud,
        designate_date=date(date.today().year-7,2,1),   
    )
    proud_future = lgb_models.HomeStadium.objects.create(
        team=teams.kentucky,
        stadium_config=stadium_configs.proud_future,
        designate_date=date(date.today().year+7,2,1),   
    )
    home_stad_list = [
        "bart",
        "springs",
        "banks",
        "proud",
        "proud_future",
    ]
    HomeStadiumObj = namedtuple("HomeStadiumObj", home_stad_list)
    return HomeStadiumObj(
        bart=bart,
        springs=springs,
        banks=banks,
        proud=proud,
        proud_future=proud_future,
    )