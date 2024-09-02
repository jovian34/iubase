import pytest
from django.urls import reverse
from datetime import date

from accounts.tests.fixtures import logged_user_schwarbs
from live_game_blog.tests.fixtures import teams
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.form_data import forms
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.summer import (
    summer_assign,
    summer_leagues,
    summer_teams,
)


this_year = date.today().year


@pytest.mark.django_db
def test_add_transaction_partial_post_adds_transaction(
    client, players, teams, annual_rosters, logged_user_schwarbs, prof_orgs, forms
):
    response = client.post(
        reverse("add_transaction", args=[players.brayden_risedorph.pk]),
        forms.risedorph_drafted,
        follow=True,
    )
    assert response.status_code == 200
    assert "Drafted" in str(response.content)
    assert "July 17" in str(response.content)
    assert 'href="https://www.mlb.com/draft/tracker"'
    response = client.get(reverse("drafted_players", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert "Brayden Risedorph" in str(response.content)
    assert "he can get a bonus value of $150,000" in str(response.content)
    assert "Expected to go over slot value." in str(response.content)
    assert "Arizona Diamondbacks" in str(response.content)


@pytest.mark.django_db
def test_add_transaction_partial_get_renders_form_fields(
    client, players, teams, logged_user_schwarbs
):
    response = client.get(
        reverse(
            "add_transaction",
            args=[players.nick_mitchell.pk],
        )
    )
    assert response.status_code == 200
    assert "Transaction Event" in str(response.content)
    assert "Transaction Date" in str(response.content)
    assert f"{this_year}" in str(response.content)


@pytest.mark.django_db
def test_add_transaction_partial_get_redirects_not_logged_in(client, players, teams):
    response = client.get(
        reverse(
            "add_transaction",
            args=[players.nick_mitchell.pk],
        )
    )
    assert response.status_code == 302