import pytest

from collections import namedtuple

from player_tracking.models import SummerLeague, SummerTeam, SummerAssign
from player_tracking.tests.fixtures.players import players


@pytest.fixture
def summer_leagues():
    nw = SummerLeague.objects.create(league="Northwoods")
    in_fr = SummerLeague.objects.create(league="International Friendship")
    SummerLeagueObj = namedtuple("SummerLeagueObj", "nw in_fr")
    return SummerLeagueObj(nw=nw, in_fr=in_fr)


@pytest.fixture
def summer_teams():
    gb = SummerTeam.objects.create(
        name="Green Bay",
        mascot="Rockers",
    )
    usa = SummerTeam.objects.create(
        name="Team USA",
        mascot="Americans",
    )
    SummerTeamObj = namedtuple("SummerTeamObj", "gb usa")
    return SummerTeamObj(gb=gb, usa=usa)


@pytest.fixture
def summer_assign(players, summer_leagues, summer_teams):
    dt_gb_2024 = SummerAssign.objects.create(
        player=players.dt2022,
        summer_year=2024,
        summer_league=summer_leagues.in_fr,
        summer_team=summer_teams.usa,
    )
    SummerAssignObj = namedtuple("SummerAssignObj", "dt_gb_2024")
    return SummerAssignObj(dt_gb_2024=dt_gb_2024)
