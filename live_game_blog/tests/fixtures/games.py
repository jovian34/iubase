import pytest

from collections import namedtuple
from django.utils import timezone
import datetime

from live_game_blog.models import Game, Team, Scoreboard, BlogEntry
from accounts.models import CustomUser
from accounts.tests.fixtures import (
    user_not_logged_in,
    user_iubase17,
    logged_user_schwarbs,
    superuser_houston,
)
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs


@pytest.fixture
def games(client, teams, stadiums, stadium_configs):
    iu_duke = Game.objects.create(
        home_team=teams.duke,
        away_team=teams.indiana,
        neutral_site=True,
        first_pitch=(timezone.now() + datetime.timedelta(days=1)),
        stadium_config=stadium_configs.surprise,
    )
    iu_duke_ly = Game.objects.create(
        home_team=teams.duke,
        away_team=teams.indiana,
        neutral_site=True,
        first_pitch=(timezone.now() - datetime.timedelta(days=365)),
        stadium_config=stadium_configs.surprise,
    )
    iu_duke_23_fall = Game.objects.create(
        home_team=teams.duke,
        away_team=teams.indiana,
        neutral_site=True,
        first_pitch=datetime.datetime(
            2023, 10, 4, 21, 5, 00, tzinfo=datetime.timezone.utc
        ),
        stadium_config=stadium_configs.surprise,
    )
    iu_duke_69_spring = Game.objects.create(
        home_team=teams.duke,
        away_team=teams.indiana,
        neutral_site=True,
        first_pitch=datetime.datetime(
            2069, 2, 24, 21, 5, 00, tzinfo=datetime.timezone.utc
        ),
        stadium_config=stadium_configs.surprise,
    )
    iu_coastal = Game.objects.create(
        home_team=teams.coastal,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=(timezone.now() + datetime.timedelta(days=2, hours=7)),
        stadium_config=stadium_configs.springs,
    )
    iu_coastal_ip = Game.objects.create(
        home_team=teams.coastal,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=(timezone.now() - datetime.timedelta(hours=1)),
        event="Pre-season Tournament",
        first_pitch_wind_angle=20,
        stadium_config=stadium_configs.springs,
        live_stats="http://stats.statbroadcast.com/broadcast/?id=499358",
    )
    iu_coastal_tom = Game.objects.create(
        home_team=teams.coastal,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=(timezone.now() + datetime.timedelta(hours=27)),
        event="Pre-season Tournament",
        stadium_config=stadium_configs.springs,
    )
    iu_gm = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.gm,
        neutral_site=True,
        first_pitch=(timezone.now() + datetime.timedelta(days=3)),
        stadium_config=stadium_configs.surprise,
    )
    iu_iowa = Game.objects.create(
        home_team=teams.iowa,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=datetime.datetime(
            timezone.now().year + 3, 4, 4, 21, 5, 00, tzinfo=datetime.timezone.utc
        ),
        stadium_config=stadium_configs.banks,
    )
    iu_mo_rain = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.miami_oh,
        neutral_site=False,
        first_pitch=(timezone.now() + datetime.timedelta(days=-315)),
        stadium_config=stadium_configs.bart,
    )
    iu_mo = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.miami_oh,
        neutral_site=False,
        first_pitch=(timezone.now() + datetime.timedelta(days=5)),
        stadium_config=stadium_configs.bart,
    )
    iu_uk_mon = Game.objects.create(
        home_team=teams.kentucky,
        home_seed=1,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=(timezone.now() - datetime.timedelta(days=300)),
        live_stats="https://t.co/Odg1uF46xM",
    )
    iu_uk_sun = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.kentucky,
        neutral_site=True,
        first_pitch=(timezone.now() - datetime.timedelta(days=301)),
        stadium_config=stadium_configs.surprise,
    )
    iu_uk_sat = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.kentucky,
        neutral_site=True,
        first_pitch=(timezone.now() - datetime.timedelta(days=302)),
        stadium_config=stadium_configs.surprise,
    )
    iu_gm_fall = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.gm,
        neutral_site=False,
        event="Fall exhibition",
        first_pitch=(timezone.now() + datetime.timedelta(days=1)),
        stadium_config=stadium_configs.bart,
    )
    iu_uk_far_future = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.kentucky,
        neutral_site=False,
        first_pitch=(timezone.now() + datetime.timedelta(days=8)),
        stadium_config=stadium_configs.bart,
    )
    game_list = [
        "iu_duke",
        "iu_duke_ly",
        "iu_duke_23_fall",
        "iu_duke_69_spring",
        "iu_coastal",
        "iu_coastal_ip",
        "iu_coastal_tom",
        "iu_gm",
        "iu_mo",
        "iu_iowa",
        "iu_mo_rain",
        "iu_uk_mon",
        "iu_uk_sun",
        "iu_uk_sat",
        "iu_gm_fall",
        "iu_uk_far_future",
    ]
    GameObj = namedtuple("GameObj", game_list)
    return GameObj(
        iu_duke=iu_duke,
        iu_duke_ly=iu_duke_ly,
        iu_duke_23_fall=iu_duke_23_fall,
        iu_duke_69_spring=iu_duke_69_spring,
        iu_coastal=iu_coastal,
        iu_coastal_ip=iu_coastal_ip,
        iu_coastal_tom=iu_coastal_tom,
        iu_gm=iu_gm,
        iu_mo=iu_mo,
        iu_iowa=iu_iowa,
        iu_mo_rain=iu_mo_rain,
        iu_uk_mon=iu_uk_mon,
        iu_uk_sun=iu_uk_sun,
        iu_uk_sat=iu_uk_sat,
        iu_gm_fall=iu_gm_fall,
        iu_uk_far_future=iu_uk_far_future,
    )
