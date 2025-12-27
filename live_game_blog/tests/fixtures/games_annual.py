import pytest
import pytz

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

eastern = pytz.timezone('America/New_York')

if datetime.date.today().month > 8:
    spring_year = datetime.date.today().year + 1
else:
    spring_year = datetime.date.today().year


@pytest.fixture
def games_annual(client, teams, stadiums, stadium_configs):
    iu_ky_ly = Game.objects.create(
        home_team=teams.kentucky,
        away_team=teams.indiana,
        neutral_site=True,
        first_pitch=eastern.localize(datetime.datetime(spring_year-1, 2, 15, 18, 0, 0, 0)),
        stadium_config=stadium_configs.surprise,
    )
    iu_duke = Game.objects.create(
        home_team=teams.duke,
        away_team=teams.indiana,
        neutral_site=True,
        first_pitch=eastern.localize(datetime.datetime(spring_year, 5, 15, 18, 0, 0, 0)),
        stadium_config=stadium_configs.surprise,
    )
    iu_iowa = Game.objects.create(
        home_team=teams.iowa,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=eastern.localize(datetime.datetime(spring_year, 3, 15, 19, 0, 0, 0)),
        stadium_config=stadium_configs.banks,
    )
    iu_mo = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.miami_oh,
        neutral_site=False,
        first_pitch=eastern.localize(datetime.datetime(spring_year, 3, 18, 14, 0, 0, 0)),
        stadium_config=stadium_configs.bart,
    )
    iu_coastal_ny = Game.objects.create(
        home_team=teams.coastal,
        away_team=teams.indiana,
        neutral_site=True,
        first_pitch=eastern.localize(datetime.datetime(spring_year+1, 2, 15, 18, 0, 0, 0)),
        stadium_config=stadium_configs.surprise,
    )
    game_list = [
        "iu_ky_ly",
        "iu_duke",
        "iu_iowa",
        "iu_mo",
        "iu_coastal_ny",
    ]
    GameObj = namedtuple("GameObj", game_list)
    return GameObj(
        iu_ky_ly=iu_ky_ly,
        iu_duke=iu_duke,
        iu_mo=iu_mo,
        iu_iowa=iu_iowa,
        iu_coastal_ny=iu_coastal_ny,
    )
