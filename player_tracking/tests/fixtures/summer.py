import pytest

from collections import namedtuple

from player_tracking.models import SummerLeague, SummerTeam, SummerAssign
from player_tracking.tests.fixtures.players import players


@pytest.fixture
def summer_leagues():
    nw = SummerLeague.objects.create(
        league="Northwoods"
    )
    SummerLeagueObj = namedtuple(
        "SummerLeagueObj",
        "nw"
    )
    return SummerLeagueObj(
        nw=nw,
    )

@pytest.fixture
def summer_teams():
    gb = SummerTeam.objects.create(
        name="Green Bay",
        mascot="Rockers",
    )
    SummerTeamObj = namedtuple(
        "SummerTeamObj",
        "gb"
    )
    return SummerTeamObj(
        gb=gb
    )

@pytest.fixture
def summer_assign(players, summer_leagues, summer_teams):
    dt_gb_2023 = SummerAssign.objects.create(
        player=players.dt2022,
        summer_year=2023,
        summer_league=summer_leagues.nw,
        summer_team=summer_teams.gb,
    )
    SummerAssignObj = namedtuple(
        "SummerAssignObj",
        "dt_gb_2023"
    )
    return SummerAssignObj(
        dt_gb_2023=dt_gb_2023
    )