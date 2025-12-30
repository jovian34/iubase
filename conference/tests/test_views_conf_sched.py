import pytest
import datetime
from django import urls

from live_game_blog.tests.fixtures.teams import teams
from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.conf_teams import conf_teams
from conference.tests.fixtures.conf_series import conf_series

from conference import year



@pytest.mark.django_db
def test_current_year_b1g_schedule_renders(client, teams, conferences, conf_teams, conf_series):
    response = client.get(urls.reverse("conf_schedule", args=[year.get_spring_year()]))
    assert response.status_code == 200
    assert "2026 B1G Schedule" in response.content.decode()
    assert "March 7-9" in response.content.decode()
    assert "Iowa at Indiana" in response.content.decode()
