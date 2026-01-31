import pytest

from django import urls

from accounts.tests.fixtures import logged_user_schwarbs, user_not_logged_in


@pytest.mark.django_db
def test_picks_register_redirects_not_logged_in(client, user_not_logged_in):
    response = client.get(urls.reverse("picks_register"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_picks_register_renders_template(client, logged_user_schwarbs):
    response = client.get(urls.reverse("picks_register"))
    assert response.status_code == 200