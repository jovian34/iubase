import pytest

from django import urls

from live_game_blog.tests.fixtures.teams import teams
from accounts.tests.fixtures import logged_user_schwarbs


@pytest.mark.django_db
def test_add_stadium_data_renders_with_form(admin_client, teams):
    response = admin_client.get(urls.reverse("add_home_stadium_data", args=[teams.kentucky.pk]))
    assert response.status_code == 200
    assert "Add Home Stadium Data for Kentucky" in str(response.content)
    assert "Address" in str(response.content)
    assert "Latitude" in str(response.content)
    assert "Full name of the stadium" in str(response.content)
    assert "Out to centerfield orientation" in str(response.content)
    assert "Which side is the home team dugout?" in str(response.content)
    assert "Date stadium was set to this configuration (including name)" in str(response.content)
    assert "Date this configuration became exclusive home field" in str(response.content)


@pytest.mark.django_db
def test_add_stadium_data_fails_wo_perms(client, teams, logged_user_schwarbs):
    response = client.get(urls.reverse("add_home_stadium_data", args=[teams.kentucky.pk]))
    assert response.status_code == 403

