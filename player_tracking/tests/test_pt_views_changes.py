import pytest
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.forms import forms
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
from accounts.tests.fixtures import (
    user_not_logged_in,
    user_iubase17,
    logged_user_schwarbs,
)

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
def test_set_player_properties_produces_correct_html_output(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    assert "Devin Taylor (None-None)" in str(response.content)
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("players"), follow=True)
    # see test_set_player_properties_produces_correct_end_date_typical_case for correct year values
    assert f"Devin Taylor ({this_year - 1}-{this_year + 2})" in str(response.content)


@pytest.mark.django_db
def test_set_player_properties_produces_correct_end_date_drafted(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    nick = Player.objects.get(pk=players.nick_mitchell.pk)
    assert not nick.first_spring or nick.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    nick = Player.objects.get(pk=players.nick_mitchell.pk)
    assert nick.first_spring == this_year
    assert nick.last_spring == this_year


@pytest.mark.django_db
def test_set_player_properties_produces_correct_end_date_redshirt_transfer(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    cole = Player.objects.get(pk=players.cole_gilley.pk)
    assert not cole.first_spring or cole.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    cole = Player.objects.get(pk=players.cole_gilley.pk)
    assert cole.first_spring == this_year + 1
    assert cole.last_spring == this_year + 1


@pytest.mark.django_db
def test_set_player_properties_ends_portal_entrant_immediately(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    brooks = Player.objects.get(pk=players.brooks_ey.pk)
    assert not brooks.first_spring or brooks.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    brooks = Player.objects.get(pk=players.brooks_ey.pk)
    assert brooks.first_spring == this_year
    assert brooks.last_spring == this_year


@pytest.mark.django_db
def test_set_player_properties_properly_limits_redshirt_years(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    """
    Jack was rostered at "Duke" for four years, but was injured for the
    first three of those. In the fixture he is given a clock waiver in year two
    This is often assigned retroactively by the NCAA
    Without this he would end this year. If the logic allowed more than one
    redshirt normally he would end in two years.
    """
    response = client.get(reverse("players"), follow=True)
    jack = Player.objects.get(pk=players.jack_moffitt.pk)
    assert not jack.first_spring or jack.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    jack = Player.objects.get(pk=players.jack_moffitt.pk)
    assert jack.first_spring == this_year
    assert jack.last_spring == this_year + 1


@pytest.mark.django_db
def test_set_player_properties_properly_ends_eligible_player_who_is_now_staff(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    """
    Nathan Ball is a freshman player in this test who fails to make 
    the spring roster, and becomes a manager instead.
    """
    response = client.get(reverse("players"), follow=True)
    nate = Player.objects.get(pk=players.nate_ball.pk)
    assert not nate.first_spring or nate.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    nate = Player.objects.get(pk=players.nate_ball.pk)
    assert nate.first_spring == this_year
    assert nate.last_spring == this_year


@pytest.mark.django_db
def test_set_player_properties_properly_resets_drafted_not_signed(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    grant = Player.objects.get(pk=players.grant_hollister.pk)
    assert not grant.first_spring or grant.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    grant = Player.objects.get(pk=players.grant_hollister.pk)
    assert grant.first_spring == this_year + 1
    assert grant.last_spring == this_year + 4


@pytest.mark.django_db
def test_set_player_properties_properly_sets_start_for_early_juco_commit(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    holton = Player.objects.get(pk=players.holton_compton.pk)
    assert not holton.first_spring or holton.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    holton = Player.objects.get(pk=players.holton_compton.pk)
    assert holton.first_spring == this_year + 1
    assert holton.last_spring == this_year + 2


@pytest.mark.django_db
def test_set_player_properties_asks_for_password_not_logged_in(
    client, players, annual_rosters, transactions
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    assert "Password" in str(response.content)


@pytest.mark.django_db
def test_set_player_properties_produces_correct_end_date_typical_case(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    devin = Player.objects.get(pk=players.devin_taylor.pk)
    assert not devin.first_spring or devin.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    devin = Player.objects.get(pk=players.devin_taylor.pk)
    assert devin.first_spring == this_year - 1
    assert devin.last_spring == this_year + 2


@pytest.mark.django_db
def test_add_summer_assignment_get_redirects_not_logged_in(client, players, summer_leagues, summer_teams):
    response = client.get(
        reverse("add_summer_assignment", args=[players.devin_taylor]),
        follow=True,
    )
    assert response.status_code == 200
    assert "Password" in str(response.content)


@pytest.mark.django_db
def test_add_summer_assignment_get_renders_form(client, players, summer_leagues, summer_teams, logged_user_schwarbs):
    response = client.get(
        reverse("add_summer_assignment", args=[str(players.devin_taylor.pk)])
    )
    assert response.status_code == 200
    assert "Summer Year" in str(response.content)


@pytest.mark.django_db
def test_add_summer_assignment_post_adds_assignment(client, players, summer_leagues, summer_teams, logged_user_schwarbs, forms):
    response = client.post(
        reverse("add_summer_assignment", args=[str(players.brayden_risedorph.pk)]),
        forms.summer_assignment_new,
        follow=True,
    )
    assert response.status_code == 200
    assert "Green Bay" in str(response.content)

