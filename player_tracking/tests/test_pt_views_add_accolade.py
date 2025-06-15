import pytest
from django.urls import reverse

from datetime import date

from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.form_data import forms
from player_tracking.tests.fixtures.summer import summer_leagues, summer_teams, summer_assign
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.accolades import accolades
from live_game_blog.tests.fixtures.teams import teams
from accounts.tests.fixtures import logged_user_schwarbs, user_not_logged_in

from player_tracking import models as pt_models

this_year = date.today().year


@pytest.mark.django_db
def test_add_accolade_partial_redirects_not_logged_in(client, players, user_not_logged_in):
    response = client.get(
        reverse("add_accolade", args=[str(players.devin_taylor.pk)]),
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_accolade_partial_asks_for_password_not_logged_in(client, players, user_not_logged_in):
    response = client.get(
        reverse("add_accolade", args=[str(players.devin_taylor.pk)]),
        follow=True,
    )
    assert "Password:" in str(response.content)


@pytest.mark.django_db
def test_add_accolade_partial_get_renders_form(client, players, logged_user_schwarbs):
    response = client.get(
        reverse("add_accolade", args=[str(players.devin_taylor.pk)]),
    )
    assert response.status_code == 200
    assert "Name of accolade" in str(response.content)
    assert "Date issued" in str(response.content)
    assert "Sponsor Organization" in str(response.content)
    assert "Detailed description" in str(response.content)
    assert "Web link for announcement" in str(response.content)
    assert "Applicable college roster" in str(response.content)
    assert "Applicable summer assignment" in str(response.content)


@pytest.mark.django_db
def test_add_accolade_partial_get_renders_form_with_only_one_players_rosters(client, players, annual_rosters, teams, logged_user_schwarbs):
    response = client.get(
        reverse("add_accolade", args=[str(players.devin_taylor.pk)]),
    )
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_add_accolade_partial_get_renders_form_with_only_one_players_rosters_manual_url(client, players, annual_rosters, teams, logged_user_schwarbs):
    response = client.get(
        f"/player_tracking/add_accolade/{players.devin_taylor.pk}/"
    )
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_add_accolade_partial_post_redirects(client, players, logged_user_schwarbs, summer_leagues, summer_teams, summer_assign, forms, prof_orgs):
    response = client.post(
        reverse("add_accolade", args=[str(players.devin_taylor.pk)]),
        forms.dt_foy,
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_accolade_partial_post_redirects_to_player_page(client, players, logged_user_schwarbs, summer_leagues, summer_teams, forms, prof_orgs):
    response = client.post(
        reverse("add_accolade", args=[str(players.devin_taylor.pk)]),
        forms.dt_foy,
        follow=True,
    )
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_add_accolade_partial_post_submits_form_data(client, players, logged_user_schwarbs, summer_leagues, summer_teams, summer_assign, forms, prof_orgs, accolades):
    response = client.post(
        reverse("add_accolade", args=[players.devin_taylor.pk]),
        forms.dt_foy,
        follow=True,
    )
    assert response.status_code == 200
    assert "B1G First Team All-Conference Outfielder" in str(response.content)
    assert "B1G Freshman of the Year" in str(response.content)


@pytest.mark.django_db
def test_add_college_accolade_partial_post_adds_correct_data(client, players, logged_user_schwarbs, summer_leagues, summer_teams, summer_assign, forms, prof_orgs, accolades, annual_rosters):
    response = client.post(
        reverse("add_accolade", args=[players.devin_taylor.pk]),
        forms.dt_foy,
    )
    assert response.status_code == 302
    foy = pt_models.Accolade.objects.get(description="devindude")
    assert foy.annual_roster == annual_rosters.dt_fresh
    assert foy.player == players.devin_taylor
    assert foy.award_date == date(this_year-1, 5, 23)
    assert foy.award_org == "B1G"
    assert not foy.summer_assign
    assert str(foy.citation) == "https://iuhoosiers.com/news/2023/5/23/baseball-b1g-honors-for-taylor-and-co"


@pytest.mark.django_db
def test_add_summer_accolade_partial_post_adds_correct_data(client, players, logged_user_schwarbs, summer_leagues, summer_teams, summer_assign, forms, prof_orgs, accolades, annual_rosters):
    response = client.post(
        reverse("add_accolade", args=[players.devin_taylor.pk]),
        forms.dt_roy,
    )
    assert response.status_code == 302
    roy = pt_models.Accolade.objects.get(description="devinrookie")
    assert roy.summer_assign == summer_assign.dt_kg_ly
    assert roy.player == players.devin_taylor
    assert roy.award_date == date(this_year-1, 7, 23)
    assert roy.award_org == "Northwoods League"
    assert not roy.annual_roster
    assert str(roy.citation) == "https://www.idsnews.com/article/2023/08/indiana-baseball-devin-taylor-necbl-rookie-of-the-year-tyler-cerny-appalachian-league"

