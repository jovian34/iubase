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
def conf_series_two_way_h2h(conferences, conf_teams, teams):
    indiana_mich=conf_models.ConfSeries.objects.create(
        home_team=teams.indiana,
        away_team=teams.mich,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=3,
        away_wins=0,
    )
    mich_iowa=conf_models.ConfSeries.objects.create(
        home_team=teams.mich,
        away_team=teams.iowa,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=3,
        away_wins=0,
    )
    minny_indiana=conf_models.ConfSeries.objects.create(
        home_team=teams.minny,
        away_team=teams.indiana,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=3,
        away_wins=0,
    )
    series_list = [
        "indiana_mich",
        "mich_iowa",
        "minny_indiana",
    ]

    ConfSeriesObj = namedtuple("ConfSeriesObj", series_list)

    return ConfSeriesObj(
        indiana_mich=indiana_mich,
        mich_iowa=mich_iowa,
        minny_indiana=minny_indiana,
    )