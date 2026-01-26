import pytest

from django import urls

from accounts.tests.fixtures import logged_user_schwarbs, user_not_logged_in


def test_picks_register_redirects_not_logged_in(client, user_not_logged_in):
    response = client(urls.reverse("picks_register"))
    assert response.status_code == 302