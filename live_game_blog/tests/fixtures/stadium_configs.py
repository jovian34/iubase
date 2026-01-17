import pytest

from collections import namedtuple
from datetime import date, timedelta

from live_game_blog import models as lgb_models
from live_game_blog.tests.fixtures.stadiums import stadiums

from conference.logic import year

@pytest.fixture
def stadium_configs(client, stadiums):
    bart = lgb_models.StadiumConfig.objects.create(
        stadium_name="Bart Kaufman Field",
        stadium=stadiums.bart,
        config_date=date(year.get_spring_year()-12,3,1),
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
    surprise = lgb_models.StadiumConfig.objects.create(
        stadium_name="Surprise Stadium",
        stadium=stadiums.surprise,
        config_date=date(year.get_spring_year()-23,12,8),
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
    springs = lgb_models.StadiumConfig.objects.create(
        stadium_name="Springs Brooks Stadium - Vrooman Field",
        stadium=stadiums.springs,
        config_date=date(year.get_spring_year()-10,2,1),
        surface_inf="natural",
        surface_out="natural",
        surface_mound="natural",
        photo="https://live.staticflickr.com/65535/53540501122_aaaf00f1d4_c.jpg",
        left=310,
        center=380,
        right=310,
        capacity=5300,
        orientation=126,
    )
    banks = lgb_models.StadiumConfig.objects.create(
        stadium_name="Duane Banks Field",
        stadium=stadiums.banks,
        config_date=date(year.get_spring_year()-15,3,1),
        surface_inf="artificial",
        surface_out="artificial",
        surface_mound="artificial",
        photo="https://assets.corridorbusiness.com/2022/12/Duane-Banks-Baseball-Stadium.png",
        left=325,
        center=400,
        right=325,
        capacity=3000,
        orientation=27,
        home_dugout="first",
    )
    proud = lgb_models.StadiumConfig.objects.create(
        stadium_name="Kentucky Proud Park",
        stadium=stadiums.proud,
        config_date=date(year.get_spring_year()-7,2,1),
        surface_inf="artificial",
        surface_out="artificial",
        surface_mound="natural",
        photo="https://live.staticflickr.com/65535/52947179552_349321280b_c.jpg",
        left=335,
        center=400,
        right=320,
        capacity=7000,
        orientation=100,
        home_dugout="third",
    )
    proud_future = lgb_models.StadiumConfig.objects.create(
        stadium_name="Kentucky Very Proud Park",
        stadium=stadiums.proud,
        config_date=date(year.get_spring_year()+7,2,1),
        surface_inf="artificial",
        surface_out="artificial",
        surface_mound="artificial",
        photo="https://live.staticflickr.com/65535/52947179552_349321280b_c.jpg",
        left=335,
        center=400,
        right=320,
        capacity=7000,
        orientation=100,
        home_dugout="third",
    )
    config_list = [
        "bart",
        "surprise",
        "springs",
        "banks",
        "proud",
        "proud_future",
    ]
    StadiumConfigObj = namedtuple("StadiumConfigObj", config_list)
    return StadiumConfigObj(
        bart=bart,
        surprise=surprise,
        springs=springs,
        banks=banks,
        proud=proud,
        proud_future=proud_future,
    )