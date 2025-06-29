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


@pytest.fixture
def games(client, teams):
    iu_duke = Game.objects.create(
        home_team=teams.duke,
        away_team=teams.indiana,
        neutral_site=True,
        first_pitch=(timezone.now() + datetime.timedelta(days=1)),
    )
    iu_duke_ly = Game.objects.create(
        home_team=teams.duke,
        away_team=teams.indiana,
        neutral_site=True,
        first_pitch=(timezone.now() - datetime.timedelta(days=365)),
    )
    iu_duke_23_fall = Game.objects.create(
        home_team=teams.duke,
        away_team=teams.indiana,
        neutral_site=True,
        first_pitch=datetime.datetime(
            2023, 10, 4, 21, 5, 00, tzinfo=datetime.timezone.utc
        ),
    )
    iu_coastal = Game.objects.create(
        home_team=teams.coastal,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=(timezone.now() + datetime.timedelta(days=2, hours=7)),
    )
    iu_coastal_ip = Game.objects.create(
        home_team=teams.coastal,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=(timezone.now() - datetime.timedelta(hours=1)),
    )
    iu_gm = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.gm,
        neutral_site=True,
        first_pitch=(timezone.now() + datetime.timedelta(days=3)),
    )
    iu_iowa = Game.objects.create(
        home_team=teams.iowa,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=datetime.datetime(
            timezone.now().year + 3, 4, 4, 21, 5, 00, tzinfo=datetime.timezone.utc
        ),
    )
    iu_mo_rain = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.miami_oh,
        neutral_site=False,
        first_pitch=(timezone.now() + datetime.timedelta(days=-315)),
    )
    iu_mo = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.miami_oh,
        neutral_site=False,
        first_pitch=(timezone.now() + datetime.timedelta(days=5)),
    )
    iu_uk_mon = Game.objects.create(
        home_team=teams.kentucky,
        home_seed=1,
        away_team=teams.indiana,
        neutral_site=False,
        first_pitch=(timezone.now() - datetime.timedelta(days=300)),
    )
    iu_uk_sun = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.kentucky,
        neutral_site=True,
        first_pitch=(timezone.now() - datetime.timedelta(days=301)),
    )
    iu_uk_sat = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.kentucky,
        neutral_site=True,
        first_pitch=(timezone.now() - datetime.timedelta(days=302)),
    )
    iu_gm_fall = Game.objects.create(
        home_team=teams.indiana,
        away_team=teams.gm,
        neutral_site=False,
        event="Fall exhibition",
        first_pitch=(timezone.now() + datetime.timedelta(days=1)),
    )
    GameObj = namedtuple(
        "GameObj",
        "iu_duke iu_duke_ly iu_duke_23_fall iu_coastal iu_coastal_ip iu_gm iu_mo iu_iowa iu_mo_rain iu_uk_mon iu_uk_sun iu_uk_sat iu_gm_fall",
    )
    return GameObj(
        iu_duke=iu_duke,
        iu_duke_ly=iu_duke_ly,
        iu_duke_23_fall=iu_duke_23_fall,
        iu_coastal=iu_coastal,
        iu_coastal_ip=iu_coastal_ip,
        iu_gm=iu_gm,
        iu_mo=iu_mo,
        iu_iowa=iu_iowa,
        iu_mo_rain=iu_mo_rain,
        iu_uk_mon=iu_uk_mon,
        iu_uk_sun=iu_uk_sun,
        iu_uk_sat=iu_uk_sat,
        iu_gm_fall=iu_gm_fall,
    )
