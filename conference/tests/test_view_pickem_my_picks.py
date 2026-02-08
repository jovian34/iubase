import pytest

from django import urls

from conference.logic import year

from accounts.tests.fixtures import staff_josh, staff_chris, staff_cass, superuser_houston, logged_user_schwarbs, user_not_logged_in, random_guy
from conference.tests.fixtures.pick_reg_annual import pick_reg_annual
from conference.tests.fixtures.picks import picks
from conference.tests.fixtures.conf_series_current import conf_series_current
from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.conf_teams import conf_teams
from conference.tests.fixtures.conf_series_three_way_rpi import conf_series_three_way_rpi
from live_game_blog.tests.fixtures.teams import teams


@pytest.mark.django_db
def test_pickem_my_pickem_redirects_not_logged_in(client, user_not_logged_in):
    response = client.get(urls.reverse("my_pickem", args=[year.get_this_year()]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_pickem_my_pickem_redirects_and_asks_for_google_login_not_logged_in(client, user_not_logged_in):
    response = client.get(
        urls.reverse("my_pickem", args=[year.get_this_year()]),
        follow=True,
    )
    assert response.status_code == 200
    assert "Sign In Via Google" in response.content.decode()


@pytest.mark.django_db
def test_pickem_my_pickem_renders_template(client, staff_josh, pick_reg_annual):
    response = client.get(urls.reverse("my_pickem", args=[year.get_this_year()]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_pickem_my_pickem_forwards_to_register_if_not_registered(client, random_guy):
    response = client.get(urls.reverse("my_pickem", args=[year.get_this_year()]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_pickem_my_pickem_renders_picks(client, logged_user_schwarbs, pick_reg_annual, picks):
    client.force_login(logged_user_schwarbs)
    response = client.get(urls.reverse("my_pickem", args=[year.get_this_year()]))
    assert response.status_code == 200
    assert "&#x2713;" in response.content.decode()