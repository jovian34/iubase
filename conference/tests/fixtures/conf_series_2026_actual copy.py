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
def conf_series_2026_actual(conferences, conf_teams, teams):
    usc_ill=conf_models.ConfSeries.objects.create(
        home_team=teams.usc,
        away_team=teams.ill,
        start_date=datetime.date(spring_year,3,6),
        home_wins=3,
        away_wins=0,
    )

    neb_sparty=conf_models.ConfSeries.objects.create(
        home_team=teams.neb,
        away_team=teams.sparty,
        start_date=datetime.date(spring_year,3,6),
        home_wins=3,
        away_wins=0,
    )

    boilers_ore=conf_models.ConfSeries.objects.create(
        home_team=teams.boilers,
        away_team=teams.ore,
        start_date=datetime.date(spring_year,3,6),
        home_wins=1,
        away_wins=2,
    )

    osu_ucla=conf_models.ConfSeries.objects.create(
        home_team=teams.osu,
        away_team=teams.ucla,
        start_date=datetime.date(spring_year,3,6),
        home_wins=0,
        away_wins=3,
    )

    indiana_wash=conf_models.ConfSeries.objects.create(
        home_team=teams.indiana,
        away_team=teams.wash,
        start_date=datetime.date(spring_year,3,6),
        home_wins=1,
        away_wins=2,
    )

    ore_indiana=conf_models.ConfSeries.objects.create(
        home_team=teams.ore,
        away_team=teams.indiana,
        start_date=datetime.date(spring_year,3,13),
        home_wins=3,
        away_wins=0,
    )

    psu_iowa=conf_models.ConfSeries.objects.create(
        home_team=teams.psu,
        away_team=teams.iowa,
        start_date=datetime.date(spring_year,3,13),
        home_wins=1,
        away_wins=2,
    )

    ucla_mich=conf_models.ConfSeries.objects.create(
        home_team=teams.ucla,
        away_team=teams.mich,
        start_date=datetime.date(spring_year,3,13),
        home_wins=3,
        away_wins=0,
    )

    rut_sparty=conf_models.ConfSeries.objects.create(
        home_team=teams.rut,
        away_team=teams.sparty,
        start_date=datetime.date(spring_year,3,13),
        home_wins=2,
        away_wins=1,
    )

    ill_minny=conf_models.ConfSeries.objects.create(
        home_team=teams.ill,
        away_team=teams.minny,
        start_date=datetime.date(spring_year,3,13),
        home_wins=2,
        away_wins=1,
    )

    wash_osu=conf_models.ConfSeries.objects.create(
        home_team=teams.wash,
        away_team=teams.osu,
        start_date=datetime.date(spring_year,3,13),
        home_wins=2,
        away_wins=1,
    )

    terps_boilers=conf_models.ConfSeries.objects.create(
        home_team=teams.terps,
        away_team=teams.boilers,
        start_date=datetime.date(spring_year,3,13),
        home_wins=1,
        away_wins=2,
    )

    nw_usc=conf_models.ConfSeries.objects.create(
        home_team=teams.nw,
        away_team=teams.usc,
        start_date=datetime.date(spring_year,3,13),
        home_wins=1,
        away_wins=2,
    )

    sparty_iowa=conf_models.ConfSeries.objects.create(
        home_team=teams.sparty,
        away_team=teams.iowa,
        start_date=datetime.date(spring_year,3,20),
        home_wins=2,
        away_wins=1,
    )

    ucla_terps=conf_models.ConfSeries.objects.create(
        home_team=teams.ucla,
        away_team=teams.terps,
        start_date=datetime.date(spring_year,3,20),
        home_wins=3,
        away_wins=0,
    )

    indiana_minny=conf_models.ConfSeries.objects.create(
        home_team=teams.indiana,
        away_team=teams.minny,
        start_date=datetime.date(spring_year,3,20),
        home_wins=2,
        away_wins=1,
    )

    mich_neb=conf_models.ConfSeries.objects.create(
        home_team=teams.mich,
        away_team=teams.neb,
        start_date=datetime.date(spring_year,3,20),
        home_wins=1,
        away_wins=2,
    )

    ore_nw=conf_models.ConfSeries.objects.create(
        home_team=teams.ore,
        away_team=teams.nw,
        start_date=datetime.date(spring_year,3,20),
        home_wins=2,
        away_wins=1,
    )

    boilers_psu=conf_models.ConfSeries.objects.create(
        home_team=teams.boilers,
        away_team=teams.psu,
        start_date=datetime.date(spring_year,3,20),
        home_wins=2,
        away_wins=1,
    )

    ill_rut=conf_models.ConfSeries.objects.create(
        home_team=teams.ill,
        away_team=teams.rut,
        start_date=datetime.date(spring_year,3,20),
        home_wins=2,
        away_wins=1,
    )

    usc_wash=conf_models.ConfSeries.objects.create(
        home_team=teams.usc,
        away_team=teams.wash,
        start_date=datetime.date(spring_year,3,20),
        home_wins=3,
        away_wins=0,
    )

    psu_ill=conf_models.ConfSeries.objects.create(
        home_team=teams.psu,
        away_team=teams.ill,
        start_date=datetime.date(spring_year,3,27),
        home_wins=1,
        away_wins=2,
    )

    neb_indiana=conf_models.ConfSeries.objects.create(
        home_team=teams.neb,
        away_team=teams.indiana,
        start_date=datetime.date(spring_year,3,27),
        home_wins=3,
        away_wins=0,
    )

    rut_mich=conf_models.ConfSeries.objects.create(
        home_team=teams.rut,
        away_team=teams.mich,
        start_date=datetime.date(spring_year,3,27),
        home_wins=1,
        away_wins=2,
    )

    wash_nw=conf_models.ConfSeries.objects.create(
        home_team=teams.wash,
        away_team=teams.nw,
        start_date=datetime.date(spring_year,3,27),
        home_wins=2,
        away_wins=1,
    )

    minny_osu=conf_models.ConfSeries.objects.create(
        home_team=teams.minny,
        away_team=teams.osu,
        start_date=datetime.date(spring_year,3,27),
        home_wins=0,
        away_wins=3,
    )

    sparty_boilers=conf_models.ConfSeries.objects.create(
        home_team=teams.sparty,
        away_team=teams.boilers,
        start_date=datetime.date(spring_year,3,27),
        home_wins=1,
        away_wins=2,
    )

    iowa_ucla=conf_models.ConfSeries.objects.create(
        home_team=teams.iowa,
        away_team=teams.ucla,
        start_date=datetime.date(spring_year,3,27),
        home_wins=0,
        away_wins=3,
    )

    terps_usc=conf_models.ConfSeries.objects.create(
        home_team=teams.terps,
        away_team=teams.usc,
        start_date=datetime.date(spring_year,3,27),
        home_wins=1,
        away_wins=2,
    )

    boilers_ill=conf_models.ConfSeries.objects.create(
        home_team=teams.boilers,
        away_team=teams.ill,
        start_date=datetime.date(spring_year,4,3),
        home_wins=2,
        away_wins=1,
    )

    osu_terps=conf_models.ConfSeries.objects.create(
        home_team=teams.osu,
        away_team=teams.terps,
        start_date=datetime.date(spring_year,4,3),
        home_wins=3,
        away_wins=0,
    )

    nw_sparty=conf_models.ConfSeries.objects.create(
        home_team=teams.nw,
        away_team=teams.sparty,
        start_date=datetime.date(spring_year,4,3),
        home_wins=2,
        away_wins=1,
    )

    iowa_minny=conf_models.ConfSeries.objects.create(
        home_team=teams.iowa,
        away_team=teams.minny,
        start_date=datetime.date(spring_year,4,3),
        home_wins=2,
        away_wins=1,
    )

    mich_ore=conf_models.ConfSeries.objects.create(
        home_team=teams.mich,
        away_team=teams.ore,
        start_date=datetime.date(spring_year,4,3),
        home_wins=2,
        away_wins=1,
    )

    neb_psu=conf_models.ConfSeries.objects.create(
        home_team=teams.neb,
        away_team=teams.psu,
        start_date=datetime.date(spring_year,4,3),
        home_wins=3,
        away_wins=0,
    )

    indiana_rut=conf_models.ConfSeries.objects.create(
        home_team=teams.indiana,
        away_team=teams.rut,
        start_date=datetime.date(spring_year,4,3),
        home_wins=2,
        away_wins=1,
    )

    ucla_usc=conf_models.ConfSeries.objects.create(
        home_team=teams.ucla,
        away_team=teams.usc,
        start_date=datetime.date(spring_year,4,3),
        home_wins=3,
        away_wins=0,
    )

    terps_indiana=conf_models.ConfSeries.objects.create(
        home_team=teams.terps,
        away_team=teams.indiana,
        start_date=datetime.date(spring_year,4,10),
        home_wins=2,
        away_wins=1,
    )

    usc_iowa=conf_models.ConfSeries.objects.create(
        home_team=teams.usc,
        away_team=teams.iowa,
        start_date=datetime.date(spring_year,4,10),
        home_wins=3,
        away_wins=0,
    )

    sparty_mich=conf_models.ConfSeries.objects.create(
        home_team=teams.sparty,
        away_team=teams.mich,
        start_date=datetime.date(spring_year,4,10),
        home_wins=1,
        away_wins=2,
    )

    ore_neb=conf_models.ConfSeries.objects.create(
        home_team=teams.ore,
        away_team=teams.neb,
        start_date=datetime.date(spring_year,4,10),
        home_wins=2,
        away_wins=1,
    )

    osu_psu=conf_models.ConfSeries.objects.create(
        home_team=teams.osu,
        away_team=teams.psu,
        start_date=datetime.date(spring_year,4,10),
        home_wins=2,
        away_wins=1,
    )

    nw_boilers=conf_models.ConfSeries.objects.create(
        home_team=teams.nw,
        away_team=teams.boilers,
        start_date=datetime.date(spring_year,4,10),
        home_wins=0,
        away_wins=3,
    )

    rut_ucla=conf_models.ConfSeries.objects.create(
        home_team=teams.rut,
        away_team=teams.ucla,
        start_date=datetime.date(spring_year,4,10),
        home_wins=0,
        away_wins=3,
    )

    minny_wash=conf_models.ConfSeries.objects.create(
        home_team=teams.minny,
        away_team=teams.wash,
        start_date=datetime.date(spring_year,4,10),
        home_wins=2,
        away_wins=1,
    )

    iowa_terps=conf_models.ConfSeries.objects.create(
        home_team=teams.iowa,
        away_team=teams.terps,
        start_date=datetime.date(spring_year,4,17),
        home_wins=2,
        away_wins=1,
    )

    wash_sparty=conf_models.ConfSeries.objects.create(
        home_team=teams.wash,
        away_team=teams.sparty,
        start_date=datetime.date(spring_year,4,17),
        home_wins=1,
        away_wins=2,
    )

    ucla_minny=conf_models.ConfSeries.objects.create(
        home_team=teams.ucla,
        away_team=teams.minny,
        start_date=datetime.date(spring_year,4,17),
        home_wins=3,
        away_wins=0,
    )

    mich_nw=conf_models.ConfSeries.objects.create(
        home_team=teams.mich,
        away_team=teams.nw,
        start_date=datetime.date(spring_year,4,17),
        home_wins=3,
        away_wins=0,
    )

    boilers_osu=conf_models.ConfSeries.objects.create(
        home_team=teams.boilers,
        away_team=teams.osu,
        start_date=datetime.date(spring_year,4,17),
        home_wins=3,
        away_wins=0,
    )

    ill_ore=conf_models.ConfSeries.objects.create(
        home_team=teams.ill,
        away_team=teams.ore,
        start_date=datetime.date(spring_year,4,17),
        home_wins=1,
        away_wins=2,
    )

    psu_rut=conf_models.ConfSeries.objects.create(
        home_team=teams.psu,
        away_team=teams.rut,
        start_date=datetime.date(spring_year,4,17),
        home_wins=1,
        away_wins=2,
    )

    neb_usc=conf_models.ConfSeries.objects.create(
        home_team=teams.neb,
        away_team=teams.usc,
        start_date=datetime.date(spring_year,4,17),
        home_wins=3,
        away_wins=0,
    )

    indiana_iowa=conf_models.ConfSeries.objects.create(
        home_team=teams.indiana,
        away_team=teams.iowa,
        start_date=datetime.date(spring_year,4,24),
        home_wins=0,
        away_wins=3,
    )

    sparty_terps=conf_models.ConfSeries.objects.create(
        home_team=teams.sparty,
        away_team=teams.terps,
        start_date=datetime.date(spring_year,4,24),
        home_wins=2,
        away_wins=1,
    )

    ill_neb=conf_models.ConfSeries.objects.create(
        home_team=teams.ill,
        away_team=teams.neb,
        start_date=datetime.date(spring_year,4,24),
        home_wins=1,
        away_wins=2,
    )

    minny_nw=conf_models.ConfSeries.objects.create(
        home_team=teams.minny,
        away_team=teams.nw,
        start_date=datetime.date(spring_year,4,24),
        home_wins=3,
        away_wins=0,
    )

    rut_osu=conf_models.ConfSeries.objects.create(
        home_team=teams.rut,
        away_team=teams.osu,
        start_date=datetime.date(spring_year,4,24),
        home_wins=2,
        away_wins=1,
    )

    ore_psu=conf_models.ConfSeries.objects.create(
        home_team=teams.ore,
        away_team=teams.psu,
        start_date=datetime.date(spring_year,4,24),
        home_wins=3,
        away_wins=0,
    )

    usc_boilers=conf_models.ConfSeries.objects.create(
        home_team=teams.usc,
        away_team=teams.boilers,
        start_date=datetime.date(spring_year,4,24),
        home_wins=3,
        away_wins=0,
    )

    mich_wash=conf_models.ConfSeries.objects.create(
        home_team=teams.mich,
        away_team=teams.wash,
        start_date=datetime.date(spring_year,4,24),
        home_wins=2,
        away_wins=1,
    )

    iowa_ill=conf_models.ConfSeries.objects.create(
        home_team=teams.iowa,
        away_team=teams.ill,
        start_date=datetime.date(spring_year,5,1),
        home_wins=2,
        away_wins=1,
    )

    nw_indiana=conf_models.ConfSeries.objects.create(
        home_team=teams.nw,
        away_team=teams.indiana,
        start_date=datetime.date(spring_year,5,1),
        home_wins=2,
        away_wins=1,
    )

    terps_mich=conf_models.ConfSeries.objects.create(
        home_team=teams.terps,
        away_team=teams.mich,
        start_date=datetime.date(spring_year,5,1),
        home_wins=0,
        away_wins=3,
    )

    psu_minny=conf_models.ConfSeries.objects.create(
        home_team=teams.psu,
        away_team=teams.minny,
        start_date=datetime.date(spring_year,5,1),
        home_wins=1,
        away_wins=2,
    )

    osu_neb=conf_models.ConfSeries.objects.create(
        home_team=teams.osu,
        away_team=teams.neb,
        start_date=datetime.date(spring_year,5,1),
        home_wins=3,
        away_wins=0,
    )

    wash_ore=conf_models.ConfSeries.objects.create(
        home_team=teams.wash,
        away_team=teams.ore,
        start_date=datetime.date(spring_year,5,1),
        home_wins=1,
        away_wins=2,
    )

    usc_rut=conf_models.ConfSeries.objects.create(
        home_team=teams.usc,
        away_team=teams.rut,
        start_date=datetime.date(spring_year,5,1),
        home_wins=3,
        away_wins=0,
    )

    sparty_ucla=conf_models.ConfSeries.objects.create(
        home_team=teams.sparty,
        away_team=teams.ucla,
        start_date=datetime.date(spring_year,5,1),
        home_wins=0,
        away_wins=3,
    )

    boilers_indiana=conf_models.ConfSeries.objects.create(
        home_team=teams.boilers,
        away_team=teams.indiana,
        start_date=datetime.date(spring_year,5,8),
        home_wins=3,
        away_wins=0,
    )

    neb_iowa=conf_models.ConfSeries.objects.create(
        home_team=teams.neb,
        away_team=teams.iowa,
        start_date=datetime.date(spring_year,5,8),
        home_wins=3,
        away_wins=0,
    )

    rut_terps=conf_models.ConfSeries.objects.create(
        home_team=teams.rut,
        away_team=teams.terps,
        start_date=datetime.date(spring_year,5,8),
        home_wins=2,
        away_wins=1,
    )

    minny_mich=conf_models.ConfSeries.objects.create(
        home_team=teams.minny,
        away_team=teams.mich,
        start_date=datetime.date(spring_year,5,8),
        home_wins=1,
        away_wins=2,
    )

    osu_sparty=conf_models.ConfSeries.objects.create(
        home_team=teams.osu,
        away_team=teams.sparty,
        start_date=datetime.date(spring_year,5,8),
        home_wins=2,
        away_wins=1,
    )

    ill_nw=conf_models.ConfSeries.objects.create(
        home_team=teams.ill,
        away_team=teams.nw,
        start_date=datetime.date(spring_year,5,8),
        home_wins=3,
        away_wins=0,
    )

    ucla_ore=conf_models.ConfSeries.objects.create(
        home_team=teams.ucla,
        away_team=teams.ore,
        start_date=datetime.date(spring_year,5,8),
        home_wins=2,
        away_wins=1,
    )

    psu_wash=conf_models.ConfSeries.objects.create(
        home_team=teams.psu,
        away_team=teams.wash,
        start_date=datetime.date(spring_year,5,8),
        home_wins=2,
        away_wins=1,
    )

    indiana_ill=conf_models.ConfSeries.objects.create(
        home_team=teams.indiana,
        away_team=teams.ill,
        start_date=datetime.date(spring_year,5,14),
        home_wins=2,
        away_wins=1,
    )

    minny_neb=conf_models.ConfSeries.objects.create(
        home_team=teams.minny,
        away_team=teams.neb,
        start_date=datetime.date(spring_year,5,14),
        home_wins=0,
        away_wins=3,
    )

    mich_osu=conf_models.ConfSeries.objects.create(
        home_team=teams.mich,
        away_team=teams.osu,
        start_date=datetime.date(spring_year,5,14),
        home_wins=0,
        away_wins=3,
    )

    terps_psu=conf_models.ConfSeries.objects.create(
        home_team=teams.terps,
        away_team=teams.psu,
        start_date=datetime.date(spring_year,5,14),
        home_wins=2,
        away_wins=1,
    )

    iowa_boilers=conf_models.ConfSeries.objects.create(
        home_team=teams.iowa,
        away_team=teams.boilers,
        start_date=datetime.date(spring_year,5,14),
        home_wins=3,
        away_wins=0,
    )

    nw_rut=conf_models.ConfSeries.objects.create(
        home_team=teams.nw,
        away_team=teams.rut,
        start_date=datetime.date(spring_year,5,14),
        home_wins=1,
        away_wins=2,
    )

    wash_ucla=conf_models.ConfSeries.objects.create(
        home_team=teams.wash,
        away_team=teams.ucla,
        start_date=datetime.date(spring_year,5,14),
        home_wins=1,
        away_wins=2,
    )

    ore_usc=conf_models.ConfSeries.objects.create(
        home_team=teams.ore,
        away_team=teams.usc,
        start_date=datetime.date(spring_year,5,14),
        home_wins=2,
        away_wins=1,
    )

    series_list = [
        "usc_ill",
        "neb_sparty",
        "boilers_ore",
        "osu_ucla",
        "indiana_wash",
        "ore_indiana",
        "psu_iowa",
        "ucla_mich",
        "rut_sparty",
        "ill_minny",
        "wash_osu",
        "terps_boilers",
        "nw_usc",
        "sparty_iowa",
        "ucla_terps",
        "indiana_minny",
        "mich_neb",
        "ore_nw",
        "boilers_psu",
        "ill_rut",
        "usc_wash",
        "psu_ill",
        "neb_indiana",
        "rut_mich",
        "wash_nw",
        "minny_osu",
        "sparty_boilers",
        "iowa_ucla",
        "terps_usc",
        "boilers_ill",
        "osu_terps",
        "nw_sparty",
        "iowa_minny",
        "mich_ore",
        "neb_psu",
        "indiana_rut",
        "ucla_usc",
        "terps_indiana",
        "usc_iowa",
        "sparty_mich",
        "ore_neb",
        "osu_psu",
        "nw_boilers",
        "rut_ucla",
        "minny_wash",
        "iowa_terps",
        "wash_sparty",
        "ucla_minny",
        "mich_nw",
        "boilers_osu",
        "ill_ore",
        "psu_rut",
        "neb_usc",
        "indiana_iowa",
        "sparty_terps",
        "ill_neb",
        "minny_nw",
        "rut_osu",
        "ore_psu",
        "usc_boilers",
        "mich_wash",
        "iowa_ill",
        "nw_indiana",
        "terps_mich",
        "psu_minny",
        "osu_neb",
        "wash_ore",
        "usc_rut",
        "sparty_ucla",
        "boilers_indiana",
        "neb_iowa",
        "rut_terps",
        "minny_mich",
        "osu_sparty",
        "ill_nw",
        "ucla_ore",
        "psu_wash",
        "indiana_ill",
        "minny_neb",
        "mich_osu",
        "terps_psu",
        "iowa_boilers",
        "nw_rut",
        "wash_ucla",
        "ore_usc",
    ]

    ConfSeriesObj = namedtuple("ConfSeriesObj", series_list)

    return ConfSeriesObj(
        usc_ill=usc_ill,
        neb_sparty=neb_sparty,
        boilers_ore=boilers_ore,
        osu_ucla=osu_ucla,
        indiana_wash=indiana_wash,
        ore_indiana=ore_indiana,
        psu_iowa=psu_iowa,
        ucla_mich=ucla_mich,
        rut_sparty=rut_sparty,
        ill_minny=ill_minny,
        wash_osu=wash_osu,
        terps_boilers=terps_boilers,
        nw_usc=nw_usc,
        sparty_iowa=sparty_iowa,
        ucla_terps=ucla_terps,
        indiana_minny=indiana_minny,
        mich_neb=mich_neb,
        ore_nw=ore_nw,
        boilers_psu=boilers_psu,
        ill_rut=ill_rut,
        usc_wash=usc_wash,
        psu_ill=psu_ill,
        neb_indiana=neb_indiana,
        rut_mich=rut_mich,
        wash_nw=wash_nw,
        minny_osu=minny_osu,
        sparty_boilers=sparty_boilers,
        iowa_ucla=iowa_ucla,
        terps_usc=terps_usc,
        boilers_ill=boilers_ill,
        osu_terps=osu_terps,
        nw_sparty=nw_sparty,
        iowa_minny=iowa_minny,
        mich_ore=mich_ore,
        neb_psu=neb_psu,
        indiana_rut=indiana_rut,
        ucla_usc=ucla_usc,
        terps_indiana=terps_indiana,
        usc_iowa=usc_iowa,
        sparty_mich=sparty_mich,
        ore_neb=ore_neb,
        osu_psu=osu_psu,
        nw_boilers=nw_boilers,
        rut_ucla=rut_ucla,
        minny_wash=minny_wash,
        iowa_terps=iowa_terps,
        wash_sparty=wash_sparty,
        ucla_minny=ucla_minny,
        mich_nw=mich_nw,
        boilers_osu=boilers_osu,
        ill_ore=ill_ore,
        psu_rut=psu_rut,
        neb_usc=neb_usc,
        indiana_iowa=indiana_iowa,
        sparty_terps=sparty_terps,
        ill_neb=ill_neb,
        minny_nw=minny_nw,
        rut_osu=rut_osu,
        ore_psu=ore_psu,
        usc_boilers=usc_boilers,
        mich_wash=mich_wash,
        iowa_ill=iowa_ill,
        nw_indiana=nw_indiana,
        terps_mich=terps_mich,
        psu_minny=psu_minny,
        osu_neb=osu_neb,
        wash_ore=wash_ore,
        usc_rut=usc_rut,
        sparty_ucla=sparty_ucla,
        boilers_indiana=boilers_indiana,
        neb_iowa=neb_iowa,
        rut_terps=rut_terps,
        minny_mich=minny_mich,
        osu_sparty=osu_sparty,
        ill_nw=ill_nw,
        ucla_ore=ucla_ore,
        psu_wash=psu_wash,
        indiana_ill=indiana_ill,
        minny_neb=minny_neb,
        mich_osu=mich_osu,
        terps_psu=terps_psu,
        iowa_boilers=iowa_boilers,
        nw_rut=nw_rut,
        wash_ucla=wash_ucla,
        ore_usc=ore_usc,
    )