import pytest

from datetime import datetime
from player_tracking.tests.fixtures import players, transactions, annual_roster

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
def test_annual_roster_model_stored_all_fields(client, annual_roster):
    assert annual_roster.dt_2023.fall_year == 2023
    assert annual_roster.dt_2022.player.first == "Devin"
    assert annual_roster.dt_2022.jersey == 5
    assert annual_roster.dt_2023.primary_position == "OF"
    assert annual_roster.dt_2022.secondary_position == "1B"
    assert not annual_roster.dt_2023.secondary_position

@pytest.mark.django_db
def test_annual_roster_model_string_def(client, annual_roster):
    assert str(annual_roster.dt_2023) == "Devin Taylor 2023 - roster"