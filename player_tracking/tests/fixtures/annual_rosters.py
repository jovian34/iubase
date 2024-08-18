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
        player=players.devin_taylor,
        team=teams.indiana,
        jersey=5,
        primary_position="Corner Outfield",
        secondary_position="First Base",
    )
    dt_2024 = AnnualRoster.objects.create(
        spring_year=2024,
        status="Fall Roster",
        team=teams.indiana,
        player=players.devin_taylor,
        jersey=5,
        primary_position="Corner Outfield",
    )
    nm_2024 = AnnualRoster.objects.create(
        spring_year=2024,
        status="Fall Roster",
        player=players.nick_mitchell,
        team=teams.indiana,
        jersey=20,
        primary_position="Centerfield",
    )
    nm_2023 = AnnualRoster.objects.create(
        spring_year=2023,
        status="Spring Roster",
        player=players.nick_mitchell,
        team=teams.miami_oh,
        jersey=20,
        primary_position="Centerfield",
        secondary_position="Corner Outfield",
    )
    nm_2022 = AnnualRoster.objects.create(
        spring_year=2022,
        status="Spring Roster",
        player=players.nick_mitchell,
        team=teams.miami_oh,
        jersey=20,
        primary_position="Centerfield",
        secondary_position="Corner Outfield",
    )
    hc_2023 = AnnualRoster.objects.create(
        spring_year=2023,
        status="Spring Roster",
        player=players.holton_compton,
        team=teams.miami_oh,
        jersey=35,
        primary_position="Pitcher",
    )
    hc_2024 = AnnualRoster.objects.create(
        spring_year=2024,
        status="Spring Roster",
        player=players.holton_compton,
        team=teams.miami_oh,
        jersey=35,
        primary_position="Pitcher",
    )
    br_2023 = AnnualRoster.objects.create(
        spring_year=2023,
        status="Spring Roster",
        player=players.brayden_risedorph,
        team=teams.indiana,
        jersey=51,
        primary_position="Pitcher",
    )
    jm_2024 = AnnualRoster.objects.create(
        spring_year=2024,
        status="Spring Roster",
        player=players.jack_moffitt,
        team=teams.indiana,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_2023 = AnnualRoster.objects.create(
        spring_year=2023,
        status="Spring Roster",
        player=players.jack_moffitt,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_2022 = AnnualRoster.objects.create(
        spring_year=2022,
        status="On Spring Roster but did not play",
        player=players.jack_moffitt,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_2021 = AnnualRoster.objects.create(
        spring_year=2021,
        status="Redshirt with clock extension - Medical",
        player=players.jack_moffitt,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_2020 = AnnualRoster.objects.create(
        spring_year=2020,
        status="On Spring Roster but did not play",
        player=players.jack_moffitt,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )
    cg_2021 = AnnualRoster.objects.create(
        spring_year=2021,
        status="Spring Roster",
        player=players.cole_gilley,
        team=teams.gm,
        jersey=32,
        primary_position="Pitcher",
    )
    cg_2022 = AnnualRoster.objects.create(
        spring_year=2022,
        status="Not on Spring roster",
        player=players.cole_gilley,
        team=teams.gm,
        jersey=32,
        primary_position="Pitcher",
    )
    cg_2023 = AnnualRoster.objects.create(
        spring_year=2023,
        status="Spring Roster",
        player=players.cole_gilley,
        team=teams.gm,
        jersey=32,
        primary_position="Pitcher",
    )
    cg_2024 = AnnualRoster.objects.create(
        spring_year=2024,
        status="Spring Roster",
        player=players.cole_gilley,
        team=teams.gm,
        jersey=32,
        primary_position="Pitcher",
    )
    nb_2024 = AnnualRoster.objects.create(
        spring_year=2024,
        status="Not on Spring roster",
        player=players.nate_ball,
        team=teams.indiana,
        jersey=67,
        primary_position="Pitcher",
    )
    AnnualRosterObj = namedtuple(
        "AnnualRosterObj",
        "dt_2023 dt_2024 nm_2022 nm_2023 nm_2024 hc_2023 hc_2024 br_2023 jm2020 jm2021 jm2022 jm2023 jm2024 cg_2021 cg_2022 cg_2023 cg_2024 nb_2024",
    )
    return AnnualRosterObj(
        dt_2023=dt_2023,
        dt_2024=dt_2024,
        nm_2022=nm_2022,
        nm_2023=nm_2023,
        nm_2024=nm_2024,
        hc_2023=hc_2023,
        hc_2024=hc_2024,
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
        nb_2024=nb_2024,
    )
