import pytest
from django.urls import reverse
from datetime import date

from accounts.tests.fixtures import logged_user_schwarbs
from player_tracking.models import Player
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.form_data import forms
from player_tracking.tests.fixtures.players import players
from live_game_blog.tests.fixtures.teams import teams
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.summer import (
    summer_leagues,
    summer_teams,
)


this_year = date.today().year


@pytest.mark.django_db
def test_add_roster_year_partial_get_renders_form_fields(
    client, players, teams, logged_user_schwarbs
):
    response = client.get(
        reverse(
            "add_roster_year",
            args=[players.nick_mitchell.pk],
        )
    )
    assert response.status_code == 200
    assert "Spring Year" in str(response.content)
    assert "Indiana" in str(response.content)
    assert f"{this_year}" in str(response.content)


@pytest.mark.django_db
def test_add_roster_year_partial_get_redirects_not_logged_in(client, players, teams):
    response = client.get(
        reverse(
            "add_roster_year",
            args=[players.nick_mitchell.pk],
        )
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_roster_year_partial_post_adds_roster_year(
    client, players, teams, annual_rosters, logged_user_schwarbs, forms
):
    response = client.post(
        reverse("add_roster_year", args=[players.nick_mitchell.pk]),
        forms.nick_mitchell_two_years_past,
        follow=True,
    )
    assert response.status_code == 200
    assert f"{this_year} Indiana" in str(response.content)
    assert f"{this_year - 1} Miami (Ohio)" in str(response.content)
    assert f"{this_year - 2} Duke" in str(response.content)


@pytest.mark.django_db
def test_add_roster_year_partial_post_asks_for_password_not_logged_in(
    client, players, teams, annual_rosters, forms
):
    response = client.post(
        reverse("add_roster_year", args=[players.nick_mitchell.pk]),
        forms.nick_mitchell_two_years_past,
        follow=True,
    )
    assert response.status_code == 200
    assert "Password" in str(response.content)