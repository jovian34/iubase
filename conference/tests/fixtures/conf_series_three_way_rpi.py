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
def conf_series_three_way_rpi(conferences, conf_teams, teams):
    indiana_minny=conf_models.ConfSeries.objects.create(
        home_team=teams.indiana,
        away_team=teams.minny,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=2,
        away_wins=1,
    )
    neb_iowa=conf_models.ConfSeries.objects.create(
        home_team=teams.neb,
        away_team=teams.iowa,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=1,
        away_wins=2,
    )
    nw_mich=conf_models.ConfSeries.objects.create(
        home_team=teams.nw,
        away_team=teams.mich,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=1,
        away_wins=2,
    )

    series_list = [
        "indiana_minny",
        "neb_iowa",
        "nw_mich",
    ]

    ConfSeriesObj = namedtuple("ConfSeriesObj", series_list)

    return ConfSeriesObj(
        indiana_minny=indiana_minny,
        neb_iowa=neb_iowa,
        nw_mich=nw_mich,
    )