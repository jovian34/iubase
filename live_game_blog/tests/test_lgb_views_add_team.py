import pytest

from django.urls import reverse
from live_game_blog.tests.fixtures.games import logged_user_schwarbs
from live_game_blog.tests.fixtures.form_data import forms
from live_game_blog.tests.fixtures.teams import teams
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from conference.tests.fixtures.conferences import conferences
from conference import models as conf_models


@pytest.mark.django_db
def test_add_team_get_renders_form(admin_client,):
    response = admin_client.get(reverse("add_team"))
    assert response.status_code == 200
    assert "URL for the team" in str(response.content)
    assert "Add Team" in str(response.content)
    assert "Current Conference" in str(response.content)


@pytest.mark.django_db
def test_add_team_get_forbidden_with_no_add_perms(client, logged_user_schwarbs):
    response = client.get(reverse("add_team"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_team_and_verify_redirect_to_add_stadium_for_team(
    admin_client, forms, conferences
):
    response = admin_client.post(
        reverse("add_team"),
        forms.pfw,
        follow=True,
    )
    assert response.status_code == 200
    assert "Add Home Stadium Data for Purdue F" in str(response.content)


@pytest.mark.django_db
def test_add_team_and_confirm_team_is_selectable_for_add_game(
    admin_client, forms, conferences
):
    response = admin_client.post(
        reverse("add_team"),
        forms.pfw,
    )
    assert response.status_code == 302
    response = admin_client.get(reverse("add_game"))
    assert "Purdue Ft. Wayne" in str(response.content)


@pytest.mark.django_db
def test_add_team_and_confirm_conference_team_saved(
    admin_client, forms, conferences
):
    response = admin_client.post(
        reverse("add_team"),
        forms.pfw,
    )
    assert response.status_code == 302
    pfw_hor = conf_models.ConfTeam.objects.last()
    assert pfw_hor.team.team_name == "Purdue Ft. Wayne"
    assert pfw_hor.conference.abbrev == "HOR"


@pytest.mark.django_db
def test_add_team_post_redirects_and_asks_for_login_when_not_logged_in(client, forms):
    response = client.post(
        reverse("add_team"),
        forms.pfw,
    )
    assert response.status_code == 302
    response = client.post(
        reverse("add_team"),
        forms.pfw,
        follow=True,
    )
    assert response.status_code == 200
    assert "Password:" in str(response.content)


@pytest.mark.django_db
def test_add_team_post_forbidden_without_perms(client, forms, logged_user_schwarbs):
    response = client.post(
        reverse("add_team"),
        forms.pfw,
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_game_page_renders_add_team_if_staff(
    admin_client
):
    response = admin_client.get(reverse("add_game"))
    assert response.status_code == 200
    assert "Add team" in str(response.content)
