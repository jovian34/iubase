import pytest
import datetime

from django import urls

from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.conf_teams import conf_teams
from conference.tests.fixtures.form_data import forms
from live_game_blog.tests.fixtures.teams import teams

from conference import models as conf_models

spring_year = datetime.date.today().year
if datetime.date.today().month > 8:
    spring_year = spring_year + 1


@pytest.mark.django_db
def test_add_series_get_renders(admin_client, conferences, conf_teams, teams):
    response = admin_client.get(urls.reverse("add_series", args=[spring_year]))
    assert response.status_code == 200
    assert f"Add {spring_year} Conference Series" in response.content.decode()
    assert "Series start date" in response.content.decode()
    assert "Home Team" in response.content.decode()
    assert "Away Team" in response.content.decode()
    assert "Kentucky" not in response.content.decode()
    assert "Chicago" not in response.content.decode()
    assert "Indiana" in response.content.decode()
    assert "Iowa" in response.content.decode()
    assert "UCLA" in response.content.decode()
    assert "Rutgers" in response.content.decode()
    rut = response.content.decode().find("Rutgers")
    ucla = response.content.decode().find("UCLA")
    assert rut < ucla
    expected_button = f'<button type="submit" value="Submit">Add {spring_year} Conference Series<'
    assert expected_button in response.content.decode()


@pytest.mark.django_db
def test_add_series_get_renders_former_member_as_B1G_team_eighty_years_ago(admin_client, conferences, conf_teams, teams):
    response = admin_client.get(urls.reverse("add_series", args=[spring_year-80]))
    assert "Chicago" in response.content.decode()


@pytest.mark.django_db
def test_add_series_get_is_forbidden_without_perms(client):
    response = client.get(urls.reverse("add_series", args=[spring_year]))
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_series_post_stores_correct_data(admin_client, conferences, conf_teams, teams, forms):
    response = admin_client.post(
        urls.reverse("add_series", args=[spring_year-80]),
        forms.iu_ucla,
        follow=True,
    )
    assert response.status_code == 200
    series = conf_models.ConfSeries.objects.get(start_date=datetime.date(spring_year,3,21))
    assert series.away_team.team_name == "UCLA"