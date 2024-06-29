import pytest

from collections import namedtuple

from player_tracking.models import AnnualRoster
from live_game_blog.models import Team
from live_game_blog.tests.fixtures import teams
from .players import players


@pytest.fixture
def annual_rosters(players, teams):
    dt_2023 = AnnualRoster.objects.create(
        spring_year=2023,
        status="Spring Roster",
        player=players.dt2022,
        team=teams.indiana,
        jersey=5,
        primary_position="Corner Outfield",
        secondary_position="First Base",
    )
    dt_2024 = AnnualRoster.objects.create(
        spring_year=2024,
        status="Fall Roster",
        team=teams.indiana,
        player=players.dt2022,
        jersey=5,
        primary_position="Corner Outfield",
    )
    nm_2024 = AnnualRoster.objects.create(
        spring_year=2024,
        status="Fall Roster",
        player=players.nm2021,
        team=teams.indiana,
        jersey=20,
        primary_position="Centerfield",
    )
    nm_2023 = AnnualRoster.objects.create(
        spring_year=2023,
        status="Spring Roster",
        player=players.nm2021,
        team=teams.miami_oh,
        jersey=20,
        primary_position="Centerfield",
        secondary_position="Corner Outfield",
    )
    nm_2022 = AnnualRoster.objects.create(
        spring_year=2022,
        status="Spring Roster",
        player=players.nm2021,
        team=teams.miami_oh,
        jersey=20,
        primary_position="Centerfield",
        secondary_position="Corner Outfield",
    )
    br_2023 = AnnualRoster.objects.create(
        spring_year=2023,
        status="Spring Roster",
        player=players.br2022,
        team=teams.indiana,
        jersey=51,
        primary_position="Pitcher",
    )
    jm_2024 = AnnualRoster.objects.create(
        spring_year=2024,
        status="Spring Roster",
        player=players.jm2019,
        team=teams.indiana,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_2023 = AnnualRoster.objects.create(
        spring_year=2023,
        status="Spring Roster",
        player=players.jm2019,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_2022 = AnnualRoster.objects.create(
        spring_year=2022,
        status="On Spring Roster but did not play",
        player=players.jm2019,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_2021 = AnnualRoster.objects.create(
        spring_year=2021,
        status="Redshirt with clock extension - Medical",
        player=players.jm2019,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_2020 = AnnualRoster.objects.create(
        spring_year=2020,
        status="On Spring Roster but did not play",
        player=players.jm2019,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )
    cg_2021 = AnnualRoster.objects.create(
        spring_year=2021,
        status="Spring Roster",
        player=players.cg2020,
        team=teams.gm,
        jersey=32,
        primary_position="Pitcher",
    )
    cg_2022 = AnnualRoster.objects.create(
        spring_year=2022,
        status="Not on Spring roster",
        player=players.cg2020,
        team=teams.gm,
        jersey=32,
        primary_position="Pitcher",
    )   
    cg_2023 = AnnualRoster.objects.create(
        spring_year=2023,
        status="Spring Roster",
        player=players.cg2020,
        team=teams.gm,
        jersey=32,
        primary_position="Pitcher",
    )   
    cg_2024 = AnnualRoster.objects.create(
        spring_year=2024,
        status="Spring Roster",
        player=players.cg2020,
        team=teams.gm,
        jersey=32,
        primary_position="Pitcher",
    )      
    AnnualRosterObj = namedtuple(
        "AnnualRosterObj",
        "dt_2023 dt_2024 nm_2022 nm_2023 nm_2024 br_2023 jm2020 jm2021 jm2022 jm2023 jm2024 cg_2021 cg_2022 cg_2023 cg_2024"
    )
    return AnnualRosterObj(
        dt_2023=dt_2023,
        dt_2024=dt_2024,
        nm_2022=nm_2022,
        nm_2023=nm_2023,
        nm_2024=nm_2024,
        br_2023=br_2023,
        jm2020=jm_2020,
        jm2021=jm_2021,
        jm2022=jm_2022,
        jm2023=jm_2023,
        jm2024=jm_2024,
        cg_2021=cg_2021,
        cg_2022=cg_2022,
        cg_2023=cg_2023,
        cg_2024=cg_2024,
    )


