import pytest

from django import urls

from conference.logic import year
from conference import models as conf_models

from accounts.tests.fixtures import staff_josh, staff_chris, staff_cass, superuser_houston, logged_user_schwarbs, user_not_logged_in, random_guy
from conference.tests.fixtures.pick_reg_annual import pick_reg_annual
from conference.tests.fixtures.picks import picks
from conference.tests.fixtures.conf_series_current import conf_series_current
from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.conf_teams import conf_teams
from conference.tests.fixtures.conf_series_three_way_rpi import conf_series_three_way_rpi
from live_game_blog.tests.fixtures.teams import teams


@pytest.mark.django_db
def test_choose_pick_updates_pick(client, staff_josh, pick_reg_annual, picks, conf_series_current, conf_teams, conferences, teams):
    response = client.get(urls.reverse("choose_pick", args=[conf_series_current.rut_iu, teams.indiana]))
    assert response.status_code == 200
    pick = conf_models.Pick.objects.get(
        series=conf_series_current.rut_iu,
        user=pick_reg_annual.josh
    )
    assert pick.pick == teams.indiana