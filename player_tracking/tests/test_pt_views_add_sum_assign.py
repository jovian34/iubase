import pytest
from django.urls import reverse


from accounts.tests.fixtures import logged_user_schwarbs
from live_game_blog.tests.fixtures.teams import teams
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.summer import (
    summer_assign,
    summer_leagues,
    summer_teams,
)
from player_tracking.tests.fixtures.form_data import forms


@pytest.mark.django_db
def test_add_summer_assignment_get_redirects_not_logged_in(
    client, players, summer_leagues, summer_teams
):
    response = client.get(
        reverse("add_summer_assignment", args=[players.devin_taylor]),
        follow=True,
    )
    assert response.status_code == 200
    assert "Password" in str(response.content)


@pytest.mark.django_db
def test_add_summer_assignment_get_renders_form(
    client, players, summer_leagues, summer_teams, logged_user_schwarbs
):
    response = client.get(
        reverse("add_summer_assignment", args=[str(players.devin_taylor.pk)])
    )
    assert response.status_code == 200
    assert "Summer Year" in str(response.content)


@pytest.mark.django_db
def test_add_summer_assignment_post_adds_assignment(
    client, players, summer_leagues, summer_teams, logged_user_schwarbs, forms
):
    response = client.post(
        reverse("add_summer_assignment", args=[str(players.brayden_risedorph.pk)]),
        forms.summer_assignment_new,
        follow=True,
    )
    assert response.status_code == 200
    assert "Green Bay" in str(response.content)