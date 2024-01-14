import pytest

from player_tracking.tests.fixtures import players

@pytest.mark.django_db
def test_player_model_stored_all_fields(client, players):
    assert players.dt2022.first == "Devin"
    assert players.br2022.throws == "right"
    assert players.aw2023.hsgrad_year == 2023
    assert players.dt2022.home_country == "USA"

@pytest.mark.django_db
def test_player_model_string_def(client, players):
    assert str(players.dt2022) == "Devin Taylor 2022"