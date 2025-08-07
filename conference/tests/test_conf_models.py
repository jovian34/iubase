import pytest
from datetime import date

from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.conf_teams import conf_teams
from live_game_blog.tests.fixtures.teams import teams


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
    assert conf_teams.iu_b1g.fall_year_joined == date.today().year - 108


@pytest.mark.django_db
def test_conf_team_model_correct_str_def(client, conferences, teams, conf_teams):
    assert str(conf_teams.iu_b1g) == "Indiana - B1G"