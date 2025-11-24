import pytest

from collections import namedtuple

from live_game_blog import models as lgb_models


@pytest.fixture
def stadiums(client):
    bart = lgb_models.Stadium.objects.create(
        name="Bart Kaufman Field",
        address="1873 N Fee Ln",
        city="Bloomington",
        state="IN",
        country="USA",
        timezone="America/New_York",
        orientation=43,
        lat=39.18452321031082,
        long=-86.52270607828599,
    )
    surprise = lgb_models.Stadium.objects.create(
        name="Surprise Stadium",
        address="15850 N. Bullard Ave.",
        city="Surprise",
        state="AZ",
        country="USA",
        timezone="America/Phoenix",
        orientation=45,
        lat=33.62763265256799,
        long=-112.37849762588196,
    )
    stadium_list = [
        "bart",
        "surprise"
    ]
    StadiumObj = namedtuple("StadiumObj", stadium_list)
    return StadiumObj(
        bart=bart,
        surprise=surprise,
    )