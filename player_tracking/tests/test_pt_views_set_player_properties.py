import pytest
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.form_data import forms
from player_tracking.tests.fixtures.mlb_draft_date import typical_mlb_draft_date
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.views import set_player_properties
from player_tracking.models import Player
from live_game_blog.tests.fixtures.teams import teams
from accounts.models import CustomUser
from accounts.tests.fixtures import logged_user_schwarbs


this_year = date.today().year


@pytest.mark.django_db
def test_set_player_properties_forbidden_without_perms(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"),)
    assert response.status_code == 403


@pytest.mark.django_db
def test_set_player_properties_produces_correct_html_output(
    admin_client, players, annual_rosters, transactions
):
    response = admin_client.get(reverse("players"), follow=True)
    assert "Committed, but did not come to campus as a player" in str(response.content)
    response = admin_client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    assert f"{this_year - 1}-{this_year}" in str(response.content)
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_set_player_properties_correctly_sets_mid_year_transfer(
    admin_client, players, annual_rosters, transactions
):
    response = admin_client.get(reverse("players"), follow=True)
    evan_mac = Player.objects.get(pk=players.evan_mac.pk)
    assert not evan_mac.first_spring or evan_mac.last_spring
    response = admin_client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    evan_mac = Player.objects.get(pk=players.evan_mac.pk)
    assert evan_mac.first_spring == 2023
    assert evan_mac.last_spring == 2023


@pytest.mark.django_db
def test_set_player_properties_correctly_marks_via_exhaust(
    admin_client, players, annual_rosters, transactions
):
    response = admin_client.get(reverse("players"), follow=True)
    evan_mac = Player.objects.get(pk=players.evan_mac.pk)
    cole_gilley = Player.objects.get(pk=players.cole_gilley.pk)
    assert evan_mac.via_exhaust
    assert cole_gilley.via_exhaust
    response = admin_client.get(reverse("set_player_properties"), follow=True)
    evan_mac = Player.objects.get(pk=players.evan_mac.pk)
    cole_gilley = Player.objects.get(pk=players.cole_gilley.pk)
    assert not evan_mac.via_exhaust
    assert cole_gilley.via_exhaust


@pytest.mark.django_db
def test_set_player_properties_produces_correct_end_date_future_commit(
    admin_client, players, annual_rosters, transactions
):
    response = admin_client.get(reverse("players"), follow=True)
    xavier = Player.objects.get(pk=players.xavier_carrera.pk)
    assert not xavier.first_spring or xavier.last_spring
    response = admin_client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    xavier = Player.objects.get(pk=players.xavier_carrera.pk)
    assert xavier.first_spring == this_year + 2
    assert xavier.last_spring == this_year + 5


@pytest.mark.django_db
def test_set_player_properties_produces_correct_end_date_drafted(
    admin_client, players, annual_rosters, transactions
):
    response = admin_client.get(reverse("players"), follow=True)
    nick = Player.objects.get(pk=players.nick_mitchell.pk)
    assert not nick.first_spring or nick.last_spring
    response = admin_client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    nick = Player.objects.get(pk=players.nick_mitchell.pk)
    assert nick.first_spring == this_year
    assert nick.last_spring == this_year


@pytest.mark.django_db
def test_set_player_properties_properly_limits_redshirt_years(
    admin_client, players, annual_rosters, transactions
):
    """
    Jack was rostered at "Duke" for four years, but was injured for the
    first three of those. In the fixture he is given a clock waiver in year two
    This is often assigned retroactively by the NCAA
    Without this he would end this year. If the logic allowed more than one
    redshirt normally he would end in two years.
    """
    response = admin_client.get(reverse("players"), follow=True)
    jack = Player.objects.get(pk=players.jack_moffitt.pk)
    assert not jack.first_spring or jack.last_spring
    response = admin_client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    jack = Player.objects.get(pk=players.jack_moffitt.pk)
    assert jack.first_spring == this_year
    assert jack.last_spring == this_year + 1


@pytest.mark.django_db
def test_set_player_properties_properly_ends_eligible_player_who_is_now_staff(
    admin_client, players, annual_rosters, transactions
):
    """
    Nathan Ball is a freshman player in this test who fails to make
    the spring roster, and becomes a manager instead.
    """
    response = admin_client.get(reverse("players"), follow=True)
    nate = Player.objects.get(pk=players.nate_ball.pk)
    assert not nate.first_spring or nate.last_spring
    response = admin_client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    nate = Player.objects.get(pk=players.nate_ball.pk)
    assert nate.first_spring == this_year
    assert nate.last_spring == this_year


@pytest.mark.django_db
def test_set_player_properties_produces_correct_end_date_redshirt_transfer(
    admin_client, players, annual_rosters, transactions
):
    response = admin_client.get(reverse("players"), follow=True)
    cole = Player.objects.get(pk=players.cole_gilley.pk)
    assert not cole.first_spring or cole.last_spring
    response = admin_client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    cole = Player.objects.get(pk=players.cole_gilley.pk)
    assert cole.first_spring == this_year + 1
    assert cole.last_spring == this_year + 1


@pytest.mark.django_db
def test_set_player_properties_ends_portal_entrant_immediately(
    admin_client, players, annual_rosters, transactions
):
    response = admin_client.get(reverse("players"), follow=True)
    brooks = Player.objects.get(pk=players.brooks_ey.pk)
    assert not brooks.first_spring or brooks.last_spring
    response = admin_client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    brooks = Player.objects.get(pk=players.brooks_ey.pk)
    assert brooks.first_spring == this_year
    assert brooks.last_spring == this_year


@pytest.mark.django_db
def test_set_player_properties_properly_resets_drafted_not_signed(
    admin_client, players, annual_rosters, transactions
):
    response = admin_client.get(reverse("players"), follow=True)
    grant = Player.objects.get(pk=players.grant_hollister.pk)
    assert not grant.first_spring or grant.last_spring
    response = admin_client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    grant = Player.objects.get(pk=players.grant_hollister.pk)
    assert grant.first_spring == this_year + 1
    assert grant.last_spring == this_year + 4


@pytest.mark.django_db
def test_set_player_properties_properly_shows_error_for_missing_annual_roster(
    admin_client, players, annual_rosters, transactions
):
    response = admin_client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    assert f"missing roster year {this_year - 2} for Jake Stadler" in str(
        response.content
    )


@pytest.mark.django_db
def test_set_player_properties_properly_sets_start_for_early_juco_commit(
    client,
    players,
    annual_rosters,
    transactions,
):
    holton = Player.objects.get(pk=players.holton_compton.pk)
    assert not holton.first_spring or holton.last_spring
    set_player_properties.set_player_props_get_errors()
    holton = Player.objects.get(pk=players.holton_compton.pk)
    assert holton.first_spring == this_year + 1
    assert holton.last_spring == this_year + 2


@pytest.mark.django_db
def test_set_player_properties_properly_sets_no_starts_for_decommit(
    client,
    players,
    annual_rosters,
    transactions,
):
    sinke = Player.objects.get(pk=players.gibson_sinke.pk)
    assert not sinke.first_spring or sinke.last_spring
    set_player_properties.set_player_props_get_errors()
    sinke = Player.objects.get(pk=players.gibson_sinke.pk)
    assert not sinke.first_spring or sinke.last_spring


@pytest.mark.django_db
def test_set_player_properties_properly_sets_no_starts_for_future_year_decommit(
    client,
    players,
    annual_rosters,
    transactions,
):
    amalbert = Player.objects.get(pk=players.jason_amalbert.pk)
    assert not amalbert.first_spring
    assert not amalbert.last_spring
    assert amalbert.first == "Jason"
    set_player_properties.set_player_props_get_errors()
    amalbert = Player.objects.get(pk=players.jason_amalbert.pk)
    assert amalbert.first == "Jason"
    assert amalbert.first_spring == None
    assert amalbert.last_spring == None


@pytest.mark.django_db
def test_set_player_properties_asks_for_password_not_logged_in(
    client, players, annual_rosters, transactions
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    assert "Password" in str(response.content)


@pytest.mark.django_db
def test_set_player_properties_produces_correct_end_date_typical_case(
    admin_client, players, annual_rosters, transactions
):
    krafty = Player.objects.get(pk=players.ryan_kraft.pk)
    assert not krafty.first_spring or krafty.last_spring
    set_player_properties.set_player_props_get_errors()
    krafty = Player.objects.get(pk=players.ryan_kraft.pk)
    assert krafty.first_spring == this_year - 2
    assert krafty.last_spring == this_year + 2


@pytest.mark.django_db
def test_set_player_properties_produces_correct_end_date_draft_ranked(
    players, annual_rosters, transactions
):
    set_player_properties.set_player_props_get_errors()
    devin = Player.objects.get(pk=players.devin_taylor.pk)
    assert devin.first_spring == this_year - 1
    assert devin.last_spring == this_year