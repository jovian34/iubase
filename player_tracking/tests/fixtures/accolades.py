import pytest

from collections import namedtuple
from datetime import date

from player_tracking.models import Accolade
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.annual_rosters import annual_rosters


@pytest.fixture
def accolades(players, annual_rosters):
    dt_ly_b1g_first_team = Accolade.objects.create(
        player=players.devin_taylor,
        annual_roster=annual_rosters.dt_soph,
        award_date=date.today(),
        citation=None,
        name="First Team All-Conference Outfielder",
        award_org="B1G",
        description=None,
    )
    AccoladeObj = namedtuple(
        "AccoladeObj",
        "dt_ly_b1g_first_team"
    )
    return AccoladeObj(
        dt_ly_b1g_first_team=dt_ly_b1g_first_team,
    )