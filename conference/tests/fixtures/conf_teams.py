import pytest
from collections import namedtuple
from datetime import date

from conference import models as conf_models
from conference.tests.fixtures.conferences import conferences
from live_game_blog.tests.fixtures.teams import teams


@pytest.fixture
def conf_teams(client, teams, conferences):
    iu_b1g = conf_models.ConfTeam.objects.create(
        team = teams.indiana,
        conference = conferences.b1g,
        fall_year_joined = date.today().year - 108,
    )
    iowa_b1g = conf_models.ConfTeam.objects.create(
        team = teams.iowa,
        conference = conferences.b1g,
        fall_year_joined = date.today().year - 108,
    )
    ucla_p10 = conf_models.ConfTeam.objects.create(
        team = teams.ucla,
        conference = conferences.p10,
        fall_year_joined = date.today().year - 47,
    )
    ucla_p12 = conf_models.ConfTeam.objects.create(
        team = teams.ucla,
        conference = conferences.p12,
        fall_year_joined = date.today().year - 14,
    )
    ucla_b1g = conf_models.ConfTeam.objects.create(
        team = teams.ucla,
        conference = conferences.b1g,
        fall_year_joined = date.today().year - 1,
    )
    ConfTeamObj = namedtuple(
        "ConfTeamObj",
        "iu_b1g iowa_b1g ucla_p10 ucla_p12 ucla_b1g",
    )
    return ConfTeamObj(
        iu_b1g=iu_b1g,
        iowa_b1g=iowa_b1g,
        ucla_p10=ucla_p10,
        ucla_p12=ucla_p12,
        ucla_b1g=ucla_b1g,
    )