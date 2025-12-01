import pytest
import datetime

from django import urls

from live_game_blog.tests.fixtures.teams import teams
from live_game_blog.tests.fixtures.form_data import forms
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from live_game_blog.tests.fixtures.home_stadium import home_stadium
from live_game_blog import models as lgb_models
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


@pytest.mark.django_db
def test_add_stadium_data_kentucky_post_saves_form_data(admin_client, teams, forms, stadiums, stadium_configs, home_stadium):
    first_response = admin_client.get(urls.reverse("teams_wo_stad_config"))
    assert "Kentucky" in str(first_response.content)
    response = admin_client.post(
        urls.reverse("add_home_stadium_data", args=[teams.kentucky.pk]),
        forms.uk_stadium,
        follow=True,
    )
    assert response.status_code == 200
    assert "Kentucky" not in str(response.content)
    stadium = lgb_models.Stadium.objects.get(
        long=-84.50317,
    )
    stadium_config = lgb_models.StadiumConfig.objects.get(
        stadium=stadium,
    )
    ky_home_stadium_assign = lgb_models.HomeStadium.objects.get(
        stadium_config=stadium_config,
    )
    assert stadium.long == -84.50317
    assert stadium_config.orientation == 100
    assert stadium_config.stadium_name == "Kentucky Proud Park"
    assert ky_home_stadium_assign.designate_date == datetime.date(2019,2,15)

    


