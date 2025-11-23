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
        orientation="NE",
    )
    stadium_list = [
        "bart",
    ]
    StadiumObj = namedtuple("StadiumObj", stadium_list)
    return StadiumObj(
        bart=bart,
    )