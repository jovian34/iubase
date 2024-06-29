import pytest

from collections import namedtuple

from player_tracking.models import SummerLeague, SummerTeam

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
