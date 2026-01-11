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
def conf_series_three_way_common(conferences, conf_teams, teams):
    indiana_minny=conf_models.ConfSeries.objects.create(
        home_team=teams.indiana,
        away_team=teams.minny,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=3,
        away_wins=0,
    )
    minny_iowa=conf_models.ConfSeries.objects.create(
        home_team=teams.minny,
        away_team=teams.iowa,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=1,
        away_wins=2,
    )
    mich_minny=conf_models.ConfSeries.objects.create(
        home_team=teams.mich,
        away_team=teams.minny,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=1,
        away_wins=2,
    )
    boilers_indiana=conf_models.ConfSeries.objects.create(
        home_team=teams.boilers,
        away_team=teams.indiana,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=3,
        away_wins=0,
    )
    ill_iowa=conf_models.ConfSeries.objects.create(
        home_team=teams.ill,
        away_team=teams.iowa,
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
    minny_neb=conf_models.ConfSeries.objects.create(
        home_team=teams.minny,
        away_team=teams.neb,
        start_date=datetime.date(spring_year-1,3,6),
        home_wins=1.5,
        away_wins=1.5,
    )

    series_list = [
        "indiana_minny",
        "minny_iowa",
        "mich_minny",
        "boilers_indiana",
        "ill_iowa",
        "mich_neb",
        "minny_neb"
    ]

    ConfSeriesObj = namedtuple("ConfSeriesObj", series_list)

    return ConfSeriesObj(
        indiana_minny=indiana_minny,
        minny_iowa=minny_iowa,
        mich_minny=mich_minny,
        boilers_indiana=boilers_indiana,
        ill_iowa=ill_iowa,
        mich_neb=mich_neb,
        minny_neb=minny_neb,
    )