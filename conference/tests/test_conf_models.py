import pytest
import datetime

from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.conf_teams import conf_teams
from conference.tests.fixtures.conf_series_current import conf_series_current
from conference.tests.fixtures.conf_series_three_way_rpi import conf_series_three_way_rpi
from conference.tests.fixtures.picks import picks
from conference.tests.fixtures.pick_reg_annual import pick_reg_annual
from live_game_blog.tests.fixtures.teams import teams
from accounts.tests.fixtures import logged_user_schwarbs
from accounts.tests.fixtures import user_not_logged_in
from accounts.tests.fixtures import staff_josh
from accounts.tests.fixtures import staff_chris
from accounts.tests.fixtures import staff_cass
from accounts.tests.fixtures import superuser_houston

from conference.logic import year


@pytest.mark.django_db
def test_conf_model_stored_abbreviation_logo_url_and_long_name(client, conferences):
    assert conferences.b1g.abbrev == "B1G"
    assert conferences.sec.long_name == "Southeastern Conference"
    assert conferences.b1g.logo_url == "https://cdn.d1baseball.com/uploads/2023/12/21135509/big-ten-conference.png"


@pytest.mark.django_db
def test_conf_model_renders_abbrev_as_string(client, conferences):
    assert str(conferences.b1g) == "B1G"


@pytest.mark.django_db
def test_conf_team_model_stores_team_conf_and_year(client, conferences, teams, conf_teams):
    assert conf_teams.iu_b1g.team == teams.indiana
    assert conf_teams.iu_b1g.conference == conferences.b1g
    assert conf_teams.iu_b1g.fall_year_joined == datetime.date.today().year - 108


@pytest.mark.django_db
def test_conf_team_model_correct_str_def(client, conferences, teams, conf_teams):
    assert str(conf_teams.iu_b1g) == "Indiana - B1G"


@pytest.mark.django_db
def test_conf_series_model_stores_correct_fields(client, conf_teams, conferences, teams, conf_series_current):
    assert conf_series_current.iu_iowa.home_team == teams.indiana
    assert conf_series_current.iowa_ucla.start_date == datetime.date(year.get_spring_year(), 3, 14)
    assert conf_series_current.rut_iu.home_wins == 0
    assert conf_series_current.ucla_rut.away_wins == 0


@pytest.mark.django_db
def test_conf_series_model_correct_str_def(client, conf_teams, conferences, teams, conf_series_current):
    assert str(conf_series_current.rut_iu) == f"Indiana at Rutgers: March 14-16, {year.get_spring_year()}"


@pytest.mark.django_db
def test_pick_model_correct_str_def(
    conf_series_current, 
    teams, 
    logged_user_schwarbs, 
    picks, 
    user_not_logged_in, 
    conf_series_three_way_rpi,
    pick_reg_annual
    ):
    assert str(picks.ty_iu_iowa_schwarb_iu) == f"Schwarbomb: March 7, {year.get_spring_year()} - Indiana - Incomplete"
    