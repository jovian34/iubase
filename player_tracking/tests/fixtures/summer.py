import pytest
from datetime import date

from collections import namedtuple

from player_tracking.models import SummerLeague, SummerTeam, SummerAssign
from player_tracking.tests.fixtures.players import players

this_year = date.today().year


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
    kg = SummerTeam.objects.create(
        name="Kalamazoo",
        mascot="Growlers",
    )
    usa = SummerTeam.objects.create(
        name="USA",
        mascot="Collegiate National Team",
    )
    SummerTeamObj = namedtuple("SummerTeamObj", "gb kg usa")
    return SummerTeamObj(gb=gb, kg=kg, usa=usa)


@pytest.fixture
def summer_assign(players, summer_leagues, summer_teams):
    dt_usa_ty = SummerAssign.objects.create(
        player=players.devin_taylor,
        summer_year=this_year,
        summer_league=summer_leagues.in_fr,
        summer_team=summer_teams.usa,
    )
    rk_kg_ty = SummerAssign.objects.create(
        player=players.ryan_kraft,
        summer_year=this_year,
        summer_league=summer_leagues.nw,
        summer_team=summer_teams.kg,
    )
    dt_kg_ly = SummerAssign.objects.create(
        player=players.devin_taylor,
        summer_year=this_year - 1,
        summer_league=summer_leagues.nw,
        summer_team=summer_teams.kg,
    )
    SummerAssignObj = namedtuple("SummerAssignObj", "dt_usa_ty rk_kg_ty dt_kg_ly")
    return SummerAssignObj(
        dt_usa_ty=dt_usa_ty,
        rk_kg_ty=rk_kg_ty,
        dt_kg_ly=dt_kg_ly,
    )
