import pytest

from django.urls import reverse

from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.form_data import forms
from player_tracking.tests.fixtures.summer import summer_leagues, summer_teams
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.models import Player
from live_game_blog.tests.fixtures.teams import teams
from accounts.tests.fixtures import logged_user_schwarbs, user_not_logged_in


@pytest.mark.django_db
def test_edit_player_renders(client, logged_user_schwarbs, players, transactions, prof_orgs):
    response = client.get(reverse("edit_player", args=[players.devin_taylor.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_player_renders_current_info_in_form(client, logged_user_schwarbs, players, transactions, prof_orgs):
    response = client.get(reverse("edit_player", args=[players.devin_taylor.pk]))
    assert "Devin" in str(response.content)


@pytest.mark.django_db
def test_edit_player_good_post_redirects_to_player_page(client, logged_user_schwarbs, players, transactions, prof_orgs, forms, annual_rosters):
    response = client.post(
        reverse("edit_player", args=[players.devin_taylor.pk]),
        forms.devin_taylor_edited,
        follow=True,
        )
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_edit_player_good_post_adds_action_shot(client, logged_user_schwarbs, players, transactions, prof_orgs, forms, annual_rosters):
    response = client.post(
        reverse("edit_player", args=[players.devin_taylor.pk]),
        forms.devin_taylor_edited,
        follow=True,
        )
    devin = Player.objects.get(pk=players.devin_taylor.pk)
    assert devin.last == "Taylor"
    assert devin.home_state == "OH"
    assert devin.action_shot == "https://live.staticflickr.com/65535/54132418776_e7cc1bcd11_k.jpg"


@pytest.mark.django_db
def test_edit_player_post_redirects_and_makes_no_change_not_logged_in(client, user_not_logged_in, players, transactions, prof_orgs, forms, annual_rosters):
    response = client.post(
        reverse("edit_player", args=[players.devin_taylor.pk]),
        forms.devin_taylor_edited,
        follow=True,
        )
    assert "Password" in str(response.content)
    devin = Player.objects.get(pk=players.devin_taylor.pk)
    assert devin.last == "Taylor"
    assert devin.home_state != "OH"
    assert devin.action_shot != "https://live.staticflickr.com/65535/54132418776_e7cc1bcd11_k.jpg"
    
