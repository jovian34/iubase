import pytest
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.form_data import forms
from player_tracking.tests.fixtures.mlb_draft_date import mlb_draft_date
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.tests.fixtures.summer import (
    summer_assign,
    summer_leagues,
    summer_teams,
)
from player_tracking.models import Player
from live_game_blog.tests.fixtures import teams
from accounts.models import CustomUser
from accounts.tests.fixtures import logged_user_schwarbs


this_year = date.today().year


@pytest.mark.django_db
def test_add_player_form_renders(client, logged_user_schwarbs):
    response = client.get(reverse("add_player"))
    assert response.status_code == 200
    assert "First Name" in str(response.content)
    assert "Headshot or other photo file URL" in str(response.content)


@pytest.mark.django_db
def test_add_player_form_redirects_not_logged_in(client):
    response = client.get(reverse("add_player"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_player_form_adds_new_player(client, players, logged_user_schwarbs, forms):
    response = client.post(
        reverse("add_player"),
        forms.phillip_glasser_new,
        follow=True,
    )
    assert response.status_code == 200
    assert "Phillip Glasser" in str(response.content)
    phillip = Player.objects.filter(high_school="Tallmadge").last()
    assert phillip.last == "Glasser"
    assert phillip.birthdate == date(year=this_year - 25, month=12, day=3)


@pytest.mark.django_db
def test_add_player_form_asks_for_password_not_logged_in(client, players, forms):
    response = client.post(
        reverse("add_player"),
        forms.phillip_glasser_new,
        follow=True,
    )
    assert response.status_code == 200
    assert "Password" in str(response.content)
    phillip = Player.objects.filter(first="Phillip")
    assert not phillip


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
def test_add_roster_year_partial_get_redirects_not_logged_in(client, players, teams):
    response = client.get(
        reverse(
            "add_roster_year",
            args=[players.nick_mitchell.pk],
        )
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_transaction_partial_get_redirects_not_logged_in(client, players, teams):
    response = client.get(
        reverse(
            "add_transaction",
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
