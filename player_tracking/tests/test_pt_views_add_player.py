import pytest
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.form_data import forms
from player_tracking.tests.fixtures.mlb_draft_date import typical_mlb_draft_date
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.tests.fixtures.summer import (
    summer_leagues,
    summer_teams,
    summer_assign,
)
from player_tracking.models import Player
from live_game_blog.tests.fixtures.teams import teams
from accounts.models import CustomUser
from accounts.tests.fixtures import logged_user_schwarbs
from player_tracking import models as pt_models


this_year = date.today().year


@pytest.mark.django_db
def test_add_player_form_renders_form_prompt_reverse_url(admin_client):
    response = admin_client.get(reverse("add_player"))
    assert response.status_code == 200
    assert "First Name" in response.content.decode()


@pytest.mark.django_db
def test_add_player_form_renders_form_prompt_manual_url(admin_client):
    response = admin_client.get("/player_tracking/add_player/")
    assert response.status_code == 200
    assert "Portrait headshot URL" in response.content.decode()


@pytest.mark.django_db
def test_add_player_get_redirects_not_logged_in(client):
    response = client.get(reverse("add_player"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_player_get_forbidden_without_perms(client, logged_user_schwarbs):
    response = client.get(reverse("add_player"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_player_get_ask_for_password_not_logged_in(client):
    response = client.get(reverse("add_player"), follow=True)
    assert response.status_code == 200
    assert "Password:" in response.content.decode()


@pytest.mark.django_db
def test_add_player_post_form_forbidden_without_perms(client, players, logged_user_schwarbs, forms):
    response = client.post(
        reverse("add_player"),
        forms.phillip_glasser_new,
        follow=True,
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_player_post_form_adds_new_player(admin_client, players, forms):
    response = admin_client.post(
        reverse("add_player"),
        forms.phillip_glasser_new,
        follow=True,
    )
    assert response.status_code == 200
    assert "Phillip Glasser" in response.content.decode()
    phillip = Player.objects.filter(high_school="Tallmadge").last()
    assert phillip.last == "Glasser"
    assert phillip.birthdate == date(year=this_year - 25, month=12, day=3)


@pytest.mark.django_db
def test_add_player_form_adds_new_transaction(
    admin_client, players, forms
):
    response = admin_client.post(
        reverse("add_player"),
        forms.phillip_glasser_new,
        follow=True,
    )
    trans = pt_models.Transaction.objects.filter(
        player__first="Phillip", player__last="Glasser"
    ).last()
    assert trans.trans_event == "Verbal Commitment from College"


@pytest.mark.django_db
def test_add_player_form_redirects_not_logged_in(client, players, forms):
    response = client.post(
        reverse("add_player"),
        forms.phillip_glasser_new,
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_player_form_asks_for_password_not_logged_in(client, players, forms):
    response = client.post(
        reverse("add_player"),
        forms.phillip_glasser_new,
        follow=True,
    )
    assert response.status_code == 200
    assert "Password" in response.content.decode()
    phillip = Player.objects.filter(first="Phillip")
    assert not phillip
