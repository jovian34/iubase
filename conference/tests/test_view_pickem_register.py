import pytest

from django import urls

from accounts.tests.fixtures import logged_user_schwarbs, user_not_logged_in
from conference.logic import year


@pytest.mark.django_db
def test_pickem_register_redirects_not_logged_in(client, user_not_logged_in):
    response = client.get(urls.reverse("pickem_register", args=[year.get_this_year()]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_pickem_register_renders_template(client, logged_user_schwarbs):
    response = client.get(urls.reverse("pickem_register", args=[year.get_this_year()]))
    assert response.status_code == 200