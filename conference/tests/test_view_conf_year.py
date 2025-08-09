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
            kwargs = {"conf": "B1G", "spring_year": str(date.today().year)}
        )
    )
    assert response.status_code == 200
    assert "UCLA" in str(response.content)
    assert "Indiana" in str(response.content)
    assert "Iowa" in str(response.content)
    assert f"Big Ten Conference members for {str(date.today().year)}"


@pytest.mark.django_db
def test_last_year_b1g_does_not_show_ucla(client, teams, conferences, conf_teams):
    response = client.get(
        urls.reverse(
            "conf_year", 
            kwargs = {"conf": "B1G", "spring_year": str(date.today().year - 1)}
        )
    )
    assert response.status_code == 200
    assert "UCLA" not in str(response.content)
    assert "Indiana" in str(response.content)
    assert "Iowa" in str(response.content)



@pytest.mark.django_db
def test_current_year_b1g_shows_correct_member_order(client, teams, conferences, conf_teams):
    response = client.get(
        urls.reverse(
            "conf_year", 
            kwargs = {"conf": "B1G", "spring_year": str(date.today().year)}
        )
    )
    output = str(response.content)
    ucla = output.find("UCLA")
    iu = output.find("Indiana")
    assert ucla > iu