import pytest

from collections import namedtuple

from live_game_blog import models as lgb_models


@pytest.fixture
def stadiums(client):
    bart = lgb_models.Stadium.objects.create(
        address="1873 N Fee Ln",
        city="Bloomington",
        state="IN",
        country="USA",
        timezone="America/New_York",
        lat=39.18452321031082,
        long=-86.52270607828599,
    )
    surprise = lgb_models.Stadium.objects.create(
        address="15850 N. Bullard Ave.",
        city="Surprise",
        state="AZ",
        country="USA",
        timezone="America/Phoenix",
        lat=33.62763265256799,
        long=-112.37849762588196,
    )
    springs = lgb_models.Stadium.objects.create(
        address="965 One Landon Loop",
        city="Conway",
        state="SC",
        country="USA",
        timezone="America/New_York",
        lat=33.7935720398487,
        long=-79.01539998873648,
    )
    banks = lgb_models.Stadium.objects.create(
        address="960 Stadium Drive",
        city="Iowa City",
        state="IA",
        country="USA",
        timezone="America/Chicago",
        lat=41.66094077910214,
        long=-91.55491086995895,
    )
    proud = lgb_models.Stadium.objects.create(
        address="510 Wildcat Ct.",
        city="Lexington",
        state="KY",
        country="USA",
        timezone="America/New_York",
        lat=38.018220,
        long=-84.503170,
    )
    stadium_list = [
        "bart",
        "surprise",
        "springs",
        "banks",
        "proud",
    ]
    StadiumObj = namedtuple("StadiumObj", stadium_list)
    return StadiumObj(
        bart=bart,
        surprise=surprise,
        springs=springs,
        banks=banks,
        proud=proud,
    )