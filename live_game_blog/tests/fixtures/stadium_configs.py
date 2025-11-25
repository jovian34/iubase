import pytest

from collections import namedtuple
from datetime import date

from live_game_blog import models as lgb_models
from live_game_blog.tests.fixtures.stadiums import stadiums


@pytest.fixture
def stadium_configs(client, stadiums):
    bart_2013 = lgb_models.StadiumConfig.objects.create(
        stadium_name="Bart Kaufman Field",
        stadium=stadiums.bart,
        config_date=date(2013,3,1),
        surface_inf="artificial",
        surface_out="artificial",
        surface_mound="artificial",
        photo="https://live.staticflickr.com/65535/54870456854_577c2962c0_c.jpg",
        left=330,
        center=400,
        right=330,
        capacity=2500,
        orientation=45,
        home_dugout="third"
    )
    surprise_2002 = lgb_models.StadiumConfig.objects.create(
        stadium_name="Surprise Stadium",
        stadium=stadiums.surprise,
        config_date=date(2002,12,8),
        surface_inf="natural",
        surface_out="natural",
        surface_mound="natural",
        photo="https://en.wikipedia.org/wiki/Surprise_Stadium#/media/File:Surprise_Stadium_during_Spring_Training_(2023).jpg",
        left=350,
        center=400,
        right=350,
        capacity=10714,
        orientation=45,
    )
    config_list = [
        "bart_2013",
        "surprise_2002"
    ]
    StadiumConfigObj = namedtuple("StadiumConfigObj", config_list)
    return StadiumConfigObj(
        bart_2013=bart_2013,
        surprise_2002=surprise_2002,
    )