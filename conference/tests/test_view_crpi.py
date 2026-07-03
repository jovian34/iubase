import pytest
from django import urls

from conference.logic import year

from live_game_blog.tests.fixtures.teams import teams
from conference.tests.fixtures.conf_series_2026_actual import conf_series_2026_actual
from conference.tests.fixtures.conf_teams import conf_teams
from conference.tests.fixtures.conferences import conferences


@pytest.mark.django_db
def test_crpi_page_renders(client, teams, conf_series_2026_actual, conf_teams, conferences):
    response = client.get(urls.reverse("crpi", args=[year.get_spring_year()]))
    assert response.status_code == 200
    output = response.content.decode()
    assert f"{year.get_spring_year()} B1G cRPI" in output


@pytest.mark.django_db
def test_crpi_page_shows_correct_order(client, teams, conf_series_2026_actual, conf_teams, conferences):
    response = client.get(urls.reverse("crpi", args=[year.get_spring_year()]))
    assert response.status_code == 200
    output = response.content.decode()
    assert "1. UCLA" in output
    assert "6. Michigan" in output
    assert "8. Purdue" in output
    assert "17. Northwestern" in output


@pytest.mark.django_db
def test_crpi_page_shows_proper_conf_win_percentage_for_michigan(client, teams, conf_series_2026_actual, conf_teams, conferences):
    response = client.get(urls.reverse("crpi", args=[year.get_spring_year()]))
    assert response.status_code == 200
    output = response.content.decode()
    assert "Conference W%: 0.567" in output
    mich_w_pct = output.find("Conference W%: 0.567")
    mich = output.find("6. Michigan")
    iowa = output.find("7. Iowa")
    assert mich < mich_w_pct
    assert mich_w_pct < iowa


@pytest.mark.django_db
def test_crpi_page_shows_proper_crpi_for_rutgers(client, teams, conf_series_2026_actual, conf_teams, conferences):
    response = client.get(urls.reverse("crpi", args=[year.get_spring_year()]))
    assert response.status_code == 200
    output = response.content.decode()
    title = output.find(f"{year.get_spring_year()} B1G cRPI")
    rut = output.find("12. Rutgers")
    crpi = output.find("cRPI: 0.473")
    minny = output.find("13. Minnesota")
    assert title < rut
    assert rut < crpi
    assert crpi < minny

