import pytest

from django.urls import reverse
from live_game_blog.tests.fixtures.games import logged_user_schwarbs
from live_game_blog.tests.fixtures.form_data import forms
from live_game_blog.tests.fixtures.teams import teams


@pytest.mark.django_db
def test_add_team_and_confirm_team_is_selectable_for_add_game(
    client, logged_user_schwarbs, forms
):
    response = client.post(
        reverse("add_team"),
        forms.pfw,
    )
    assert response.status_code == 302
    response = client.get(reverse("add_game"))
    assert "Purdue Ft. Wayne" in str(response.content)


@pytest.mark.django_db
def test_add_team_post_asks_for_login_when_not_logged_in(client, forms):
    response = client.post(
        reverse("add_team"),
        forms.pfw,
        follow=True,
    )
    assert response.status_code == 200
    assert "Password:" in str(response.content)


@pytest.mark.django_db
def test_add_team_post_redirects_when_not_logged_in(client, forms):
    response = client.post(
        reverse("add_team"),
        forms.pfw,
    )
    assert response.status_code == 302