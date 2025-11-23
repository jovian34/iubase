import pytest

from collections import namedtuple
from datetime import date

from live_game_blog import models as lgb_models
from live_game_blog.tests.fixtures.stadiums import stadiums


@pytest.fixture
def stadium_configs(client, stadiums):
    bart_2013 = lgb_models.StadiumConfig.objects.create(
        stadium=stadiums.bart,
        config_date=date(2013,3,1),
        surface_inf="artificial",
        surface_out="artificial",
        surface_mound="artificial",
        photo="https://live.staticflickr.com/65535/54870456854_577c2962c0_c.jpg",
        left=330,
        center=400,
        right=330,
    )
    config_list = [
        "bart_2013",
    ]
    StadiumConfigObj = namedtuple("StadiumConfigObj", config_list)
    return StadiumConfigObj(
        bart_2013=bart_2013,
    )