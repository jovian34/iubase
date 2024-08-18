import pytest

from datetime import datetime
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.mlb_draft_date import mlb_draft_date
from player_tracking.tests.fixtures.summer import (
    summer_leagues,
    summer_teams,
    summer_assign,
)
from live_game_blog.tests.fixtures import teams


@pytest.mark.django_db
def test_player_model_stored_all_fields(client, players):
    assert players.devin_taylor.first == "Devin"
    assert players.brayden_risedorph.throws == "right"
    assert players.andrew_wiggins.hsgrad_year == 2023
    assert players.devin_taylor.home_country == "USA"


@pytest.mark.django_db
def test_player_model_string_def(client, players):
    assert str(players.devin_taylor) == "Devin Taylor 2022"


@pytest.mark.django_db
def test_transaction_model_stored_all_fields(client, transactions):
    assert transactions.dt_verbal.player.last == "Taylor"
    assert (
        transactions.dt_nli.trans_event == "National Letter of Intent Signed"
    )  # need to aling with current choices
    assert transactions.dt_nli.trans_date.year == 2021


@pytest.mark.django_db
def test_transaction_model_string_def(client, transactions):
    assert (
        str(transactions.dt_verbal)
        == "Devin Taylor Verbal Commitment from High School on March 2021"
    )


@pytest.mark.django_db
def test_transaction_model_get_prof_or(client, transactions):
    assert transactions.nm_draft.draft_round == 4
    assert transactions.nm_draft.prof_org.city == "Philadelphia"


@pytest.mark.django_db
def test_transaction_model_gets_comment(client, transactions):
    assert transactions.nm_signed.comment == "Bonus value was reported two days after signing."


@pytest.mark.django_db
def test_annual_roster_model_stored_all_fields(client, annual_rosters, teams):
    assert annual_rosters.dt_soph.spring_year == 2024
    assert annual_rosters.dt_fresh.player.first == "Devin"
    assert annual_rosters.dt_fresh.jersey == 5
    assert annual_rosters.dt_soph.primary_position == "Corner Outfield"
    assert annual_rosters.dt_fresh.secondary_position == "First Base"
    assert not annual_rosters.dt_soph.secondary_position


@pytest.mark.django_db
def test_annual_roster_model_string_def(client, annual_rosters, teams):
    assert str(annual_rosters.dt_soph) == "Devin Taylor 2024 - Fall Roster"


@pytest.mark.django_db
def test_mlb_draft_birthdate_string_def(client, mlb_draft_date):
    assert str(mlb_draft_date.draft_2024) == "2024: Aug 1, 2003"


@pytest.mark.django_db
def test_summer_league_string_def(client, summer_leagues):
    assert str(summer_leagues.nw) == "Northwoods"


@pytest.mark.django_db
def test_summer_team_string_def(client, summer_teams):
    assert str(summer_teams.gb) == "Green Bay Rockers"


@pytest.mark.django_db
def test_summer_assign_string_def(client, summer_assign):
    assert str(summer_assign.dt_usa_2024) == "Devin Taylor 2024 USA"


@pytest.mark.django_db
def test_prof_org_string_def(client, prof_orgs):
    assert str(prof_orgs.d_backs) == "Arizona Diamondbacks"


@pytest.mark.django_db
def test_prof_org_model_stored_all_fields(client, prof_orgs):
    assert prof_orgs.braves.city == "Atlanta"
    assert prof_orgs.phillies.mascot == "Phillies"