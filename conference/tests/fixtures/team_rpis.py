import pytest
from collections import namedtuple
import datetime

from conference import models as conf_models
from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.conf_teams import conf_teams
from live_game_blog.tests.fixtures.teams import teams

spring_year = datetime.date.today().year
if datetime.date.today().month > 8:
    spring_year = spring_year + 1

@pytest.fixture
def team_rpis(teams):
    osu_ly = conf_models.TeamRpi.objects.create(
        team=teams.osu,
        rpi_rank=232,
        spring_year=spring_year-1
    )
    minny_ly = conf_models.TeamRpi.objects.create(
        team=teams.minny,
        rpi_rank=109,
        spring_year=spring_year-1
    )
    pur_ly = conf_models.TeamRpi.objects.create(
        team=teams.boilers,
        rpi_rank=120,
        spring_year=spring_year-1
    )
    terps_ly = conf_models.TeamRpi.objects.create(
        team=teams.terps,
        rpi_rank=232,
        spring_year=spring_year-1
    )
    nw_ly = conf_models.TeamRpi.objects.create(
        team=teams.nw,
        rpi_rank=131,
        spring_year=spring_year-1
    )
    sparty_ly = conf_models.TeamRpi.objects.create(
        team=teams.sparty,
        rpi_rank=143,
        spring_year=spring_year-1
    )
    ill_ly = conf_models.TeamRpi.objects.create(
        team=teams.ill,
        rpi_rank=115,
        spring_year=spring_year-1
    )
    rut_ly = conf_models.TeamRpi.objects.create(
        team=teams.rut,
        rpi_rank=86,
        spring_year=spring_year-1
    )
    neb_ly = conf_models.TeamRpi.objects.create(
        team=teams.neb,
        rpi_rank=53,
        spring_year=spring_year-1
    )
    psu_ly = conf_models.TeamRpi.objects.create(
        team=teams.psu,
        rpi_rank=85,
        spring_year=spring_year-1
    )
    iu_ly = conf_models.TeamRpi.objects.create(
        team=teams.indiana,
        rpi_rank=68,
        spring_year=spring_year-1
    )
    mich_ly = conf_models.TeamRpi.objects.create(
        team=teams.mich,
        rpi_rank=70,
        spring_year=spring_year-1
    )
    wash_ly = conf_models.TeamRpi.objects.create(
        team=teams.wash,
        rpi_rank=78,
        spring_year=spring_year-1
    )
    usc_ly = conf_models.TeamRpi.objects.create(
        team=teams.usc,
        rpi_rank=39,
        spring_year=spring_year-1
    )
    iowa_ly = conf_models.TeamRpi.objects.create(
        team=teams.iowa,
        rpi_rank=80,
        spring_year=spring_year-1
    )
    ore_ly = conf_models.TeamRpi.objects.create(
        team=teams.ore,
        rpi_rank=20,
        spring_year=spring_year-1
    )
    ucla_ly = conf_models.TeamRpi.objects.create(
        team=teams.ucla,
        rpi_rank=10,
        spring_year=spring_year-1
    )

    team_rpi_list = [
        "osu_ly",
        "minny_ly",
        "pur_ly",
        "terps_ly",
        "nw_ly",
        "sparty_ly",
        "ill_ly",
        "rut_ly",
        "neb_ly",
        "psu_ly",
        "iu_ly",
        "mich_ly",
        "wash_ly",
        "usc_ly",
        "iowa_ly",
        "ore_ly",
        "ucla_ly",
    ]    

    TeamRpiObj = namedtuple("TeamRpiObj", team_rpi_list)

    return TeamRpiObj(
        osu_ly=osu_ly,
        minny_ly=minny_ly,
        pur_ly=pur_ly,
        terps_ly=terps_ly,
        nw_ly=nw_ly,
        sparty_ly=sparty_ly,
        ill_ly=ill_ly,
        rut_ly=rut_ly,
        neb_ly=neb_ly,
        psu_ly=psu_ly,
        iu_ly=iu_ly,
        mich_ly=mich_ly,
        wash_ly=wash_ly,
        usc_ly=usc_ly,
        iowa_ly=iowa_ly,
        ore_ly=ore_ly,
        ucla_ly=ucla_ly,
    )