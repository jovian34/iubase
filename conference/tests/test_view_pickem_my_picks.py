import pytest

from django import urls

from accounts.tests.fixtures import staff_josh, user_not_logged_in
from conference.logic import year


@pytest.mark.django_db
def test_pickem_my_pickem_redirects_not_logged_in(client, user_not_logged_in):
    response = client.get(urls.reverse("my_pickem", args=[year.get_this_year()]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_pickem_my_pickem_redirects_and_asks_for_google_login_not_logged_in(client, user_not_logged_in):
    response = client.get(urls.reverse("my_pickem", args=[year.get_this_year()]), follow=True)
    assert response.status_code == 200
    assert "Sign In Via Google" in response.content.decode()


@pytest.mark.django_db
def test_pickem_my_pickem_renders_template(client, staff_josh):
    response = client.get(urls.reverse("my_pickem", args=[year.get_this_year()]))
    assert response.status_code == 200