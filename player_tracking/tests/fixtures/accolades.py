import pytest

from collections import namedtuple
from datetime import date, timedelta

from player_tracking.models import Accolade
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.summer import summer_assign


@pytest.fixture
def accolades(players, annual_rosters, summer_assign):
    dt_ly_ps_aa_second_team = Accolade.objects.create(
        player=players.devin_taylor,
        annual_roster=annual_rosters.dt_soph,
        award_date=date.today() - timedelta(days=150),
        citation=None,
        name="Pre-season second team All-American Outfielder",
        award_org="Perfect Game",
        description=None,
    )
    dt_ly_aa_second_team = Accolade.objects.create(
        player=players.devin_taylor,
        annual_roster=annual_rosters.dt_soph,
        award_date=date.today() - timedelta(days=30),
        citation=None,
        name="2nd team All-American Outfielder",
        award_org="Perfect Game",
        description=None,
    )
    dt_ly_b1g_first_team = Accolade.objects.create(
        player=players.devin_taylor,
        annual_roster=annual_rosters.dt_soph,
        award_date=date.today() - timedelta(days=60),
        citation=None,
        name="First Team All-Conference Outfielder",
        award_org="B1G",
        description=None,
        summer_assign=None,
    )
    rk_northwoods_pitch_of_year = Accolade.objects.create(
        player=players.ryan_kraft,
        annual_roster=None,
        summer_assign=summer_assign.rk_kg_ty,
        award_date=date.today() - timedelta(days=10),
        citation="https://northwoodsleague.com/kalamazoo-growlers/ryan-kraft-award-as-the-northwoods-league-pitcher-of-the-year/",
        name="Pitcher of the Year",
        award_org="Northwoods League",
        description=None,
    )
    AccoladeObj = namedtuple(
        "AccoladeObj",
        "dt_ly_ps_aa_second_team dt_ly_aa_second_team dt_ly_b1g_first_team rk_northwoods_pitch_of_year"
    )
    return AccoladeObj(
        dt_ly_ps_aa_second_team=dt_ly_ps_aa_second_team,
        dt_ly_aa_second_team=dt_ly_aa_second_team,
        dt_ly_b1g_first_team=dt_ly_b1g_first_team,
        rk_northwoods_pitch_of_year=rk_northwoods_pitch_of_year,
    )