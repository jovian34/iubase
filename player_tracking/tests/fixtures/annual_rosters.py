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
    jm_grad = AnnualRoster.objects.create(
        spring_year=this_year,
        status="Spring Roster",
        player=players.jack_moffitt,
        team=teams.indiana,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_sr = AnnualRoster.objects.create(
        spring_year=this_year - 1,
        status="Spring Roster",
        player=players.jack_moffitt,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_jr = AnnualRoster.objects.create(
        spring_year=this_year - 2,
        status="On Spring Roster but did not play",
        player=players.jack_moffitt,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_soph = AnnualRoster.objects.create(
        spring_year=this_year - 3,
        status="Redshirt with clock extension - Medical",
        player=players.jack_moffitt,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_fresh = AnnualRoster.objects.create(
        spring_year=this_year - 4,
        status="On Spring Roster but did not play",
        player=players.jack_moffitt,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )
    cg_fresh = AnnualRoster.objects.create(
        spring_year=this_year - 3,
        status="Spring Roster",
        player=players.cole_gilley,
        team=teams.gm,
        jersey=32,
        primary_position="Pitcher",
    )
    cg_soph = AnnualRoster.objects.create(
        spring_year=this_year - 2,
        status="Not on Spring roster",
        player=players.cole_gilley,
        team=teams.gm,
        jersey=32,
        primary_position="Pitcher",
    )
    cg_jr = AnnualRoster.objects.create(
        spring_year=this_year - 1,
        status="Spring Roster",
        player=players.cole_gilley,
        team=teams.gm,
        jersey=32,
        primary_position="Pitcher",
    )
    cg_sr = AnnualRoster.objects.create(
        spring_year=this_year,
        status="Spring Roster",
        player=players.cole_gilley,
        team=teams.gm,
        jersey=32,
        primary_position="Pitcher",
    )
    nb_fresh = AnnualRoster.objects.create(
        spring_year=this_year,
        status="Not on Spring roster",
        player=players.nate_ball,
        team=teams.indiana,
        jersey=67,
        primary_position="Pitcher",
    )
    AnnualRosterObj = namedtuple(
        "AnnualRosterObj",
        "dt_fresh dt_soph nm_fresh nm_soph nm_jr hc_fresh hc_soph br_fresh jm_fresh jm_soph jm_jr jm_sr jm2024 cg_fresh cg_soph cg_jr cg_sr nb_fresh",
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
        jm_fresh=jm_fresh,
        jm_soph=jm_soph,
        jm_jr=jm_jr,
        jm_sr=jm_sr,
        jm2024=jm_grad,
        cg_fresh=cg_fresh,
        cg_soph=cg_soph,
        cg_jr=cg_jr,
        cg_sr=cg_sr,
        nb_fresh=nb_fresh,
    )
