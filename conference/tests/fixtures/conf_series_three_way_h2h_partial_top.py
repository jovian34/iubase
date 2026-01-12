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
def conf_series_three_way_h2h_partial_top(conferences, conf_teams, teams):
    indiana_mich=conf_models.ConfSeries.objects.create(
        home_team=teams.indiana,
        away_team=teams.mich,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=2,
        away_wins=1,
    )
    iowa_indiana=conf_models.ConfSeries.objects.create(
        home_team=teams.iowa,
        away_team=teams.indiana,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=1,
        away_wins=2,
    )
    boilers_indiana=conf_models.ConfSeries.objects.create(
        home_team=teams.boilers,
        away_team=teams.indiana,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=2,
        away_wins=0,
    )
    iowa_minny=conf_models.ConfSeries.objects.create(
        home_team=teams.iowa,
        away_team=teams.minny,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=2,
        away_wins=1,
    )
    mich_neb=conf_models.ConfSeries.objects.create(
        home_team=teams.mich,
        away_team=teams.neb,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=2,
        away_wins=1,
    )

    series_list = [
        "indiana_mich",
        "iowa_indiana",
        "boilers_indiana",
        "iowa_minny",
        "mich_neb",
    ]

    ConfSeriesObj = namedtuple("ConfSeriesObj", series_list)

    return ConfSeriesObj(
        indiana_mich=indiana_mich,
        iowa_indiana=iowa_indiana,
        boilers_indiana=boilers_indiana,
        iowa_minny=iowa_minny,
        mich_neb=mich_neb,
    )