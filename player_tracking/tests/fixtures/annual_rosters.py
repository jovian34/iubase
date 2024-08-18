import pytest

from collections import namedtuple
from datetime import date

from player_tracking.models import AnnualRoster
from live_game_blog.models import Team
from live_game_blog.tests.fixtures import teams
from .players import players

this_year = date.today().year

@pytest.fixture
def annual_rosters(players, teams):
    dt_fresh = AnnualRoster.objects.create(
        spring_year=this_year - 1,
        status="Spring Roster",
        player=players.devin_taylor,
        team=teams.indiana,
        jersey=5,
        primary_position="Corner Outfield",
        secondary_position="First Base",
    )
    dt_soph = AnnualRoster.objects.create(
        spring_year=this_year,
        status="Fall Roster",
        team=teams.indiana,
        player=players.devin_taylor,
        jersey=5,
        primary_position="Corner Outfield",
    )
    nm_jr = AnnualRoster.objects.create(
        spring_year=this_year,
        status="Fall Roster",
        player=players.nick_mitchell,
        team=teams.indiana,
        jersey=20,
        primary_position="Centerfield",
    )
    nm_soph = AnnualRoster.objects.create(
        spring_year=this_year - 1,
        status="Spring Roster",
        player=players.nick_mitchell,
        team=teams.miami_oh,
        jersey=20,
        primary_position="Centerfield",
        secondary_position="Corner Outfield",
    )
    nm_fresh = AnnualRoster.objects.create(
        spring_year=this_year - 2,
        status="Spring Roster",
        player=players.nick_mitchell,
        team=teams.miami_oh,
        jersey=20,
        primary_position="Centerfield",
        secondary_position="Corner Outfield",
    )
    hc_fresh = AnnualRoster.objects.create(
        spring_year=this_year - 1,
        status="Spring Roster",
        player=players.holton_compton,
        team=teams.miami_oh,
        jersey=35,
        primary_position="Pitcher",
    )
    hc_soph = AnnualRoster.objects.create(
        spring_year=this_year,
        status="Spring Roster",
        player=players.holton_compton,
        team=teams.miami_oh,
        jersey=35,
        primary_position="Pitcher",
    )
    br_fresh = AnnualRoster.objects.create(
        spring_year=this_year - 1,
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
        "dt_fresh dt_soph nm_fresh nm_soph nm_jr hc_fresh hc_soph br_fresh jm2020 jm2021 jm2022 jm2023 jm2024 cg_2021 cg_2022 cg_2023 cg_2024 nb_2024",
    )
    return AnnualRosterObj(
        dt_fresh=dt_fresh,
        dt_soph=dt_soph,
        nm_fresh=nm_fresh,
        nm_soph=nm_soph,
        nm_jr=nm_jr,
        hc_fresh=hc_fresh,
        hc_soph=hc_soph,
        br_fresh=br_fresh,
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
