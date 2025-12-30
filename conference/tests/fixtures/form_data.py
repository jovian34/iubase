import pytz
import pytest
from collections import namedtuple
from django.utils import timezone
import datetime

from live_game_blog.tests.fixtures.teams import teams
from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.conf_teams import conf_teams
from conference.tests.fixtures.conf_series import conf_series

spring_year = datetime.date.today().year
if datetime.date.today().month > 8:
    spring_year = spring_year + 1


@pytest.fixture
def forms(teams, conferences):
    iu_ucla = {
        "home_team": teams.indiana.pk,
        "away_team": teams.ucla.pk,
        "start_date": f"{spring_year}-03-21"
    }
    form_list = [
        "iu_ucla",
    ]
    FormsObj = namedtuple("FormsObj", form_list)
    return FormsObj(
        iu_ucla=iu_ucla
    )