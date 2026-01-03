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
def conf_series(conferences, conf_teams, teams):
    iu_iowa=conf_models.ConfSeries.objects.create(
        home_team=teams.indiana,
        away_team=teams.iowa,
        start_date=datetime.date(spring_year,3,7)
    )
    ucla_rut=conf_models.ConfSeries.objects.create(
        home_team=teams.ucla,
        away_team=teams.rut,
        start_date=datetime.date(spring_year,3,7)
    )
    rut_iu=conf_models.ConfSeries.objects.create(
        home_team=teams.rut,
        away_team=teams.indiana,
        start_date=datetime.date(spring_year,3,14)
    )
    iowa_ucla=conf_models.ConfSeries.objects.create(
        home_team=teams.iowa,
        away_team=teams.ucla,
        start_date=datetime.date(spring_year,3,14)
    )

    # LY WK1 ---------------------------------------
    iu_iowa_ly=conf_models.ConfSeries.objects.create(
        home_team=teams.indiana,
        away_team=teams.iowa,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=2,
        away_wins=1,
    )
    ucla_rut_ly=conf_models.ConfSeries.objects.create(
        home_team=teams.ucla,
        away_team=teams.rut,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=2,
        away_wins=1,
    )

    # LY WK2
    rut_iu_ly=conf_models.ConfSeries.objects.create(
        home_team=teams.rut,
        away_team=teams.indiana,
        start_date=datetime.date(spring_year-1,3,13),
        home_wins=1,
        away_wins=2,
    )
    iowa_nw_ly=conf_models.ConfSeries.objects.create(
        home_team=teams.iowa,
        away_team=teams.nw,
        start_date=datetime.date(spring_year-1,3,13),
        home_wins=1,
        away_wins=2,
    )
    neb_ucla_ly=conf_models.ConfSeries.objects.create(
        home_team=teams.neb,
        away_team=teams.ucla,
        start_date=datetime.date(spring_year-1,3,13),
        home_wins=1,
        away_wins=2,
    )

    # LY WK3
    nw_rut_ly=conf_models.ConfSeries.objects.create(
        home_team=teams.nw,
        away_team=teams.rut,
        start_date=datetime.date(spring_year-1,3,20),
        home_wins=1,
        away_wins=2,
    )
    iu_ucla_ly=conf_models.ConfSeries.objects.create(
        home_team=teams.indiana,
        away_team=teams.ucla,
        start_date=datetime.date(spring_year-1,3,20),
        home_wins=0.5,
        away_wins=2.5,
    )

    series_list = [
        "iu_iowa",
        "ucla_rut",
        "rut_iu",
        "iowa_ucla",
        "iu_iowa_ly",
        "ucla_rut_ly",
        "rut_iu_ly",
        "iowa_nw_ly",
        "neb_ucla_ly",
        "nw_rut_ly",
        "iu_ucla_ly",    
    ]

    ConfSeriesObj = namedtuple("ConfSeriesObj", series_list)

    return ConfSeriesObj(
        iu_iowa=iu_iowa,
        ucla_rut=ucla_rut,
        rut_iu=rut_iu,
        iowa_ucla=iowa_ucla,
        iu_iowa_ly=iu_iowa_ly,
        ucla_rut_ly=ucla_rut_ly,
        rut_iu_ly=rut_iu_ly,
        iowa_nw_ly=iowa_nw_ly,
        neb_ucla_ly=neb_ucla_ly,
        nw_rut_ly=nw_rut_ly,
        iu_ucla_ly=iu_ucla_ly,
    )