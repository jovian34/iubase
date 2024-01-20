import pytest

from datetime import datetime
from player_tracking.tests.fixtures import players, transactions, annual_rosters
from live_game_blog.tests.fixtures import teams


@pytest.mark.django_db
def test_player_model_stored_all_fields(client, players):
    assert players.dt2022.first == "Devin"
    assert players.br2022.throws == "right"
    assert players.aw2023.hsgrad_year == 2023
    assert players.dt2022.home_country == "USA"


@pytest.mark.django_db
def test_player_model_string_def(client, players):
    assert str(players.dt2022) == "Devin Taylor 2022"


@pytest.mark.django_db
def test_transaction_model_stored_all_fields(client, transactions):
    assert transactions.dt_verbal.player.last == "Taylor"
    assert transactions.dt_nli.trans_event == "nli"
    assert transactions.dt_nli.trans_date.year == 2021


@pytest.mark.django_db
def test_transaction_model_string_def(client, transactions):
    assert str(transactions.dt_verbal) == "Devin Taylor verbal on March 2021"


@pytest.mark.django_db
def test_annual_roster_model_stored_all_fields(client, annual_rosters, teams):
    assert annual_rosters.dt_2024.spring_year == 2024
    assert annual_rosters.dt_2023.player.first == "Devin"
    assert annual_rosters.dt_2023.jersey == 5
    assert annual_rosters.dt_2024.primary_position == "Corner Outfield"
    assert annual_rosters.dt_2023.secondary_position == "First Base"
    assert not annual_rosters.dt_2024.secondary_position


@pytest.mark.django_db
def test_annual_roster_model_string_def(client, annual_rosters, teams):
    assert str(annual_rosters.dt_2024) == "Devin Taylor 2024 - Fall Roster"