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
    osu = conf_models.TeamRpi.objects.create(
        team=teams.osu,
        rpi_rank=79,
        spring_year=spring_year,
    )
    minny = conf_models.TeamRpi.objects.create(
        team=teams.minny,
        rpi_rank=94,
        spring_year=spring_year,
    )
    pur = conf_models.TeamRpi.objects.create(
        team=teams.boilers,
        rpi_rank=54,
        spring_year=spring_year,
    )
    terps = conf_models.TeamRpi.objects.create(
        team=teams.terps,
        rpi_rank=81,
        spring_year=spring_year,
    )
    nw = conf_models.TeamRpi.objects.create(
        team=teams.nw,
        rpi_rank=152,
        spring_year=spring_year,
    )
    sparty = conf_models.TeamRpi.objects.create(
        team=teams.sparty,
        rpi_rank=115,
        spring_year=spring_year,
    )
    ill = conf_models.TeamRpi.objects.create(
        team=teams.ill,
        rpi_rank=86,
        spring_year=spring_year,
    )
    rut = conf_models.TeamRpi.objects.create(
        team=teams.rut,
        rpi_rank=110,
        spring_year=spring_year,
    )
    neb = conf_models.TeamRpi.objects.create(
        team=teams.neb,
        rpi_rank=10,
        spring_year=spring_year,
    )
    psu = conf_models.TeamRpi.objects.create(
        team=teams.psu,
        rpi_rank=192,
        spring_year=spring_year,
    )
    iu = conf_models.TeamRpi.objects.create(
        team=teams.indiana,
        rpi_rank=119,
        spring_year=spring_year,
    )
    mich = conf_models.TeamRpi.objects.create(
        team=teams.mich,
        rpi_rank=52,
        spring_year=spring_year,
    )
    wash = conf_models.TeamRpi.objects.create(
        team=teams.wash,
        rpi_rank=168,
        spring_year=spring_year,
    )
    usc = conf_models.TeamRpi.objects.create(
        team=teams.usc,
        rpi_rank=8,
        spring_year=spring_year,
    )
    iowa = conf_models.TeamRpi.objects.create(
        team=teams.iowa,
        rpi_rank=62,
        spring_year=spring_year,
    )
    ore = conf_models.TeamRpi.objects.create(
        team=teams.ore,
        rpi_rank=16,
        spring_year=spring_year,
    )
    ucla = conf_models.TeamRpi.objects.create(
        team=teams.ucla,
        rpi_rank=1,
        spring_year=spring_year,
    )

    team_rpi_list = [
        "osu",
        "minny",
        "pur",
        "terps",
        "nw",
        "sparty",
        "ill",
        "rut",
        "neb",
        "psu",
        "iu",
        "mich",
        "wash",
        "usc",
        "iowa",
        "ore",
        "ucla",
    ]    

    TeamRpiObj = namedtuple("TeamRpiObj", team_rpi_list)

    return TeamRpiObj(
        osu=osu,
        minny=minny,
        pur=pur,
        terps=terps,
        nw=nw,
        sparty=sparty,
        ill=ill,
        rut=rut,
        neb=neb,
        psu=psu,
        iu=iu,
        mich=mich,
        wash=wash,
        usc=usc,
        iowa=iowa,
        ore=ore,
        ucla=ucla,
    )