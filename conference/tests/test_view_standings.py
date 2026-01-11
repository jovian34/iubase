import pytest
from django import urls

from conference import year

from live_game_blog.tests.fixtures.teams import teams
from conference.tests.fixtures.conf_series_three_way_common import conf_series_three_way_common
from conference.tests.fixtures.conf_series_three_way_h2h import conf_series_three_way_h2h
from conference.tests.fixtures.conf_series_two_way_h2h import conf_series_two_way_h2h
from conference.tests.fixtures.conf_series_three_way_h2h_partial import conf_series_three_way_h2h_partial
from conference.tests.fixtures.conf_series_three_way_rpi import conf_series_three_way_rpi
from conference.tests.fixtures.conf_teams import conf_teams
from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.team_rpis import team_rpis


@pytest.mark.django_db
def test_standings_page_renders(client, teams, team_rpis, conf_series_three_way_common, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()-1]))
    assert response.status_code == 200
    output = response.content.decode()
    assert f"{year.get_spring_year()-1} B1G Standings" in output
    assert "Indiana" in output


@pytest.mark.django_db
def test_standings_shows_high_pct_first(client, teams, team_rpis, conf_series_three_way_common, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()-1]))
    assert response.status_code == 200
    output = response.content.decode()
    boilers = output.find("Purdue")
    ill = output.find("Illinois")
    indiana = output.find("Indiana")
    mich = output.find("Michigan")
    neb = output.find("Nebraska")
    minny = output.find("Minnesota")
    assert boilers < ill
    assert ill < indiana
    assert mich < neb
    assert neb < minny


@pytest.mark.django_db
def test_standings_shows_three_way_tie_broke_by_common(client, teams, team_rpis, conf_series_three_way_common, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()-1]))
    assert response.status_code == 200
    output = response.content.decode()
    indiana = output.find("Indiana")
    iowa = output.find("Iowa")
    mich = output.find("Michigan")
    assert indiana < iowa
    assert iowa < mich


@pytest.mark.django_db
def test_standings_shows_three_way_tie_broke_by_h2h(client, teams, team_rpis, conf_series_three_way_h2h, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()-1]))
    assert response.status_code == 200
    output = response.content.decode()
    indiana = output.find("Indiana")
    iowa = output.find("Iowa")
    mich = output.find("Michigan")
    assert indiana < iowa
    assert iowa < mich


@pytest.mark.django_db
def test_standings_shows_three_way_tie_broke_by_h2h_partial(client, teams, team_rpis, conf_series_three_way_h2h_partial, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()-1]))
    assert response.status_code == 200
    output = response.content.decode()
    indiana = output.find("Indiana")
    iowa = output.find("Iowa")
    mich = output.find("Michigan")
    assert indiana < iowa
    assert mich < iowa # broke by RPI


@pytest.mark.django_db
def test_standings_shows_three_way_tie_broke_by_rpi(client, teams, team_rpis, conf_series_three_way_rpi, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()-1]))
    assert response.status_code == 200
    output = response.content.decode()
    indiana = output.find("Indiana")
    iowa = output.find("Iowa")
    mich = output.find("Michigan")
    assert mich < indiana
    assert indiana < iowa


@pytest.mark.django_db
def test_standings_shows_two_way_tie_broke_by_h2h(client, teams, team_rpis, conf_series_two_way_h2h, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()-1]))
    assert response.status_code == 200
    output = response.content.decode()
    indiana = output.find("Indiana")
    mich = output.find("Michigan")
    assert indiana < mich


    
