import pytest
import datetime
from django import urls

from live_game_blog.tests.fixtures.teams import teams
from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.conf_teams import conf_teams


spring_year = datetime.date.today().year
if datetime.date.today().month > 8:
    spring_year = spring_year + 1


@pytest.mark.django_db
def test_current_year_b1g_shows_correct_members(client, teams, conferences, conf_teams):
    response = client.get(
        urls.reverse(
            "conf_year", 
            kwargs = {"conf": "B1G", "spring_year": str(datetime.date.today().year)}
        )
    )
    assert response.status_code == 200
    assert "UCLA" in response.content.decode()
    assert "Indiana" in response.content.decode()
    assert "Iowa" in response.content.decode()
    assert f"Big Ten Conference members for {str(datetime.date.today().year)}"
    

@pytest.mark.django_db
def test_default_year_b1g_shows_correct_members(client, teams, conferences, conf_teams):
    response = client.get(urls.reverse("conf_year_default", args=["B1G"]))
    assert response.status_code == 200
    assert "UCLA" in response.content.decode()
    assert "Indiana" in response.content.decode()
    assert "Iowa" in response.content.decode()
    assert f"Big Ten Conference members for {spring_year}"


@pytest.mark.django_db
def test_last_year_b1g_does_not_show_ucla(client, teams, conferences, conf_teams):
    response = client.get(
        urls.reverse(
            "conf_year", 
            kwargs = {"conf": "B1G", "spring_year": str(datetime.date.today().year - 1)}
        )
    )
    assert response.status_code == 200
    assert "UCLA" not in response.content.decode()
    assert "Indiana" in response.content.decode()
    assert "Iowa" in response.content.decode()



@pytest.mark.django_db
def test_current_year_b1g_shows_correct_member_order(client, teams, conferences, conf_teams):
    response = client.get(
        urls.reverse(
            "conf_year", 
            kwargs = {"conf": "B1G", "spring_year": str(datetime.date.today().year)}
        )
    )
    output = response.content.decode()
    ucla = output.find("UCLA")
    iu = output.find("Indiana")
    assert ucla > iu