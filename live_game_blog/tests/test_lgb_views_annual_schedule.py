import pytest
import datetime

from django import urls

from live_game_blog.tests.fixtures.games_annual import games_annual
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from live_game_blog.tests.fixtures.teams import teams


@pytest.mark.django_db
def test_schedule_renders_selected_season_games_only(client, games_annual, stadiums, stadium_configs, teams):
    if datetime.date.today().month > 8:
        spring_year = datetime.date.today().year + 1
    else:
        spring_year = datetime.date.today().year
    response = client.get(urls.reverse("schedule", args=[spring_year]))
    assert response.status_code == 200
    assert "Miami (Ohio) <em>@</em>  Indiana" in response.content.decode()
    assert "Indiana <em>@</em>  Iowa" in response.content.decode()
    assert "Indiana <em>vs.</em>  Duke" in response.content.decode()
    assert "Kentucky" not in response.content.decode()
    assert "Coastal" not in response.content.decode()


@pytest.mark.django_db
def test_schedule_renders_selected_season_games_in_date_order(client, games_annual, stadiums, stadium_configs, teams):
    if datetime.date.today().month > 8:
        spring_year = datetime.date.today().year + 1
    else:
        spring_year = datetime.date.today().year
    response = client.get(urls.reverse("schedule", args=[spring_year]))
    assert response.status_code == 200
    output = response.content.decode()
    duke = output.find("Duke")
    iowa = output.find("Iowa")
    assert duke > iowa


@pytest.mark.django_db
def test_schedule_omits_non_iu_games(client, games_annual, stadiums, stadium_configs, teams):
    if datetime.date.today().month > 8:
        spring_year = datetime.date.today().year + 1
    else:
        spring_year = datetime.date.today().year
    response = client.get(urls.reverse("schedule", args=[spring_year]))
    assert response.status_code == 200
    assert "UCLA" not in response.content.decode()
    assert "North Carolina" not in response.content.decode()


@pytest.mark.django_db
def test_pre2026_schedule_notes_exceptions(client, games_annual, stadiums, stadium_configs, teams):
    response = client.get(urls.reverse("schedule", args=["2025"]))
    assert response.status_code == 200
    assert "*Schedules for years before 2026 are limited to games with" in response.content.decode()


@pytest.mark.django_db
def test_2026_schedule_omits_exceptions(client, games_annual, stadiums, stadium_configs, teams):
    response = client.get(urls.reverse("schedule", args=["2026"]))
    assert response.status_code == 200
    assert "*Schedules" not in response.content.decode()
    
    