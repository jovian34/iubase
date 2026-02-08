import pytest
from collections import namedtuple
import datetime

from conference import models as conf_models
from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.conf_teams import conf_teams
from live_game_blog.tests.fixtures.teams import teams

spring_year = datetime.date.today().year


@pytest.fixture
def conf_series_current_year(conferences, conf_teams, teams):
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

    series_list = [
        "iu_iowa",
        "ucla_rut",
        "rut_iu",
        "iowa_ucla",  
    ]

    ConfSeriesObj = namedtuple("ConfSeriesObj", series_list)

    return ConfSeriesObj(
        iu_iowa=iu_iowa,
        ucla_rut=ucla_rut,
        rut_iu=rut_iu,
        iowa_ucla=iowa_ucla,
    )