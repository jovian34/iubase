import pytest
from datetime import date
from django import urls

from live_game_blog.tests.fixtures.teams import teams
from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.conf_teams import conf_teams



@pytest.mark.django_db
def test_current_year_b1g_shows_correct_members(client, teams, conferences, conf_teams):
    response = client.get(
        urls.reverse(
            "conf_year", 
            args = {"conf": "b1g", "spring_year": date.today().year}
        )
    )
    assert response.status_code == 200