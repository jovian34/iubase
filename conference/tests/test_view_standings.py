import pytest
from django import urls

from conference.logic import year

from live_game_blog.tests.fixtures.teams import teams
from conference.tests.fixtures.conf_series_three_way_h2h import conf_series_three_way_h2h
from conference.tests.fixtures.conf_series_2026_actual import conf_series_2026_actual
from conference.tests.fixtures.conf_series_2026_adjusted import conf_series_2026_adjusted
from conference.tests.fixtures.conf_series_three_way_rpi import conf_series_three_way_rpi
from conference.tests.fixtures.conf_teams import conf_teams
from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.team_rpis_ly import team_rpis_ly
from conference.tests.fixtures.team_rpis import team_rpis


@pytest.mark.django_db
def test_standings_page_renders(client, teams, team_rpis, conf_series_2026_actual, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()]))
    assert response.status_code == 200
    output = response.content.decode()
    assert f"{year.get_spring_year()} B1G Standings" in output
    assert "Indiana" in output


@pytest.mark.django_db
def test_standings_shows_high_pct_first(client, teams, team_rpis, conf_series_2026_actual, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()]))
    assert response.status_code == 200
    output = response.content.decode()
    neb = output.find("Nebraska")
    boilers = output.find("Purdue")
    mich = output.find("Michigan")
    ill = output.find("Illinois")
    minny = output.find("Minnesota")
    indiana = output.find("Indiana")
    assert neb < boilers
    assert boilers < mich
    assert mich < ill
    assert ill < minny
    assert minny < indiana


@pytest.mark.django_db
def test_standings_shows_three_way_tie_broke_by_h2h(client, teams, team_rpis_ly, conf_series_three_way_h2h, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()-1]))
    assert response.status_code == 200
    output = response.content.decode()
    indiana = output.find("Indiana")
    iowa = output.find("Iowa")
    mich = output.find("Michigan")
    assert indiana < iowa
    assert iowa < mich
    assert "tie broke by head-to-head" in output


@pytest.mark.django_db
def test_standings_shows_three_way_tie_broke_by_h2h_partial_better(client, teams, team_rpis, conf_series_2026_actual, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()]))
    assert response.status_code == 200
    output = response.content.decode()
    indiana = output.find("Indiana")
    psu = output.find("Penn State")
    terps = output.find("Maryland")
    assert terps < psu
    assert terps < indiana
    assert "better record vs all in tied group" in output
    assert "worse record vs all in tied group" not in output
    best = output.find("better record vs all in tied group") # Maryland is only one this applies to
    assert terps < best # template renders team before reason note
    assert best < psu


@pytest.mark.django_db
def test_standings_shows_three_way_tie_broke_by_h2h_partial_worse(client, teams, team_rpis, conf_series_2026_adjusted, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()]))
    assert response.status_code == 200
    output = response.content.decode()
    indiana = output.find("Indiana")
    psu = output.find("Penn State")
    terps = output.find("Maryland")
    assert terps > indiana
    assert terps > psu
    assert "better record vs all in tied group" not in output
    assert "worse record vs all in tied group" in output


@pytest.mark.django_db
def test_standings_shows_two_way_tie_broke_by_record_v_team_one_through_eight(client, teams, team_rpis, conf_series_2026_actual, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()]))
    assert response.status_code == 200
    output = response.content.decode()
    sparty = output.find("Michian State")
    minny = output.find("Minnesota")
    reason = output.find("tie broke by record vs. teams in positions 1-8")
    assert sparty < reason
    assert reason < minny


@pytest.mark.django_db
def test_standings_shows_three_way_tie_broke_by_rpi(client, teams, team_rpis_ly, conf_series_three_way_rpi, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()-1]))
    assert response.status_code == 200
    output = response.content.decode()
    rpi = output.find("tie broken by RPI")
    indiana = output.find("Indiana")
    iowa = output.find("Iowa")
    mich = output.find("Michigan")
    assert mich < rpi
    assert rpi < indiana
    assert indiana < iowa


@pytest.mark.django_db
def test_standings_shows_two_way_tie_broke_by_h2h(client, teams, team_rpis, conf_series_2026_actual, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()]))
    assert response.status_code == 200
    output = response.content.decode()
    oregon = output.find("Oregon")
    usc = output.find("USC")
    assert oregon < usc
    boilers = output.find("Purdue")
    bucks = output.find("Ohio State")
    assert boilers < bucks


    
