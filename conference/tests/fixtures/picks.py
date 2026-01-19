import pytest
from collections import namedtuple

from conference import models as conf_models
from live_game_blog.tests.fixtures.teams import teams
from accounts.tests.fixtures import logged_user_schwarbs
from accounts.tests.fixtures import user_not_logged_in
from conference.tests.fixtures.conf_series_current import conf_series_current
from conference.tests.fixtures.conf_series_three_way_rpi import conf_series_three_way_rpi


@pytest.fixture
def picks(logged_user_schwarbs, user_not_logged_in, teams, conf_series_current, conf_series_three_way_rpi):
    ty_iu_iowa_schwarb_iu = conf_models.Pick.objects.create(
        user=logged_user_schwarbs,
        series=conf_series_current.iu_iowa,
        pick = teams.indiana,
    )
    ly_iu_minny_denato_min = conf_models.Pick.objects.create(
        user=user_not_logged_in,
        series=conf_series_three_way_rpi.indiana_minny,
        pick = teams.minny,
        result = "Wrong",
    )
    ly_iu_minny_schwarb_iu = conf_models.Pick.objects.create(
        user=user_not_logged_in,
        series=conf_series_three_way_rpi.indiana_minny,
        pick = teams.indiana,
        result = "Correct",
    )
    pick_list = [
        "ty_iu_iowa_schwarb_iu",
        "ly_iu_minny_denato_min",
        "ly_iu_minny_schwarb_iu",
    ]
    PickObj = namedtuple("PickObj", pick_list)
    return PickObj(
        ty_iu_iowa_schwarb_iu=ty_iu_iowa_schwarb_iu,
        ly_iu_minny_denato_min=ly_iu_minny_denato_min,
        ly_iu_minny_schwarb_iu=ly_iu_minny_schwarb_iu,
    )