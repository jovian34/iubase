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
from conference.tests.fixtures.conferences import conferences


@pytest.mark.django_db
def test_add_stadium_data_renders_with_form(admin_client, teams):
    response = admin_client.get(urls.reverse("add_home_stadium_data", args=[teams.unc.pk]))
    assert response.status_code == 200
    assert "Add Home Stadium Data for North Carolina" in response.content.decode()
    assert "Address" in response.content.decode()
    assert "Latitude" in response.content.decode()
    assert "Full name of the stadium" in response.content.decode()
    assert "Out to centerfield orientation" in response.content.decode()
    assert "Which side is the home team dugout?" in response.content.decode()
    assert "Date stadium was set to this configuration (including name)" in response.content.decode()
    assert "Date this configuration became exclusive home field" in response.content.decode()


@pytest.mark.django_db
def test_add_stadium_data_fails_wo_perms(client, teams, logged_user_schwarbs):
    response = client.get(urls.reverse("add_home_stadium_data", args=[teams.unc.pk]))
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_stadium_data_unc_post_saves_form_data(admin_client, teams, forms, stadiums, stadium_configs, home_stadium):
    first_response = admin_client.get(urls.reverse("teams_wo_stad_config"))
    assert "North Carolina" in str(first_response.content)
    response = admin_client.post(
        urls.reverse("add_home_stadium_data", args=[teams.unc.pk]),
        forms.unc_stadium,
        follow=True,
    )
    assert response.status_code == 200
    assert "North Carolina" not in response.content.decode()
    stadium = lgb_models.Stadium.objects.get(
        city="Chapel Hill",
    )
    stadium_config = lgb_models.StadiumConfig.objects.get(
        stadium=stadium,
    )
    unc_home_stadium_assign = lgb_models.HomeStadium.objects.get(
        stadium_config=stadium_config,
    )
    assert stadium.address == "235 Ridge Rd."
    assert stadium_config.orientation == 194
    assert stadium_config.stadium_name == "Bryson Field at Boshamer Stadium"
    assert unc_home_stadium_assign.designate_date == datetime.date(2009,2,2)

    


