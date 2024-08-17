import pytest
from player_tracking.tests.fixtures.players import players
from player_tracking.views.visitor_logic import group_drafted_player


@pytest.mark.django_db
def test_group_drafted_player_groups_high_school(players):
    group_drafted_player(draft_year="2024", player=players.gh2024)
    assert players.gh2024.group == "High School Signee"


@pytest.mark.django_db
def test_group_drafted_player_groups_iu(players):
    group_drafted_player(draft_year="2024", player=players.brayden_risedorph)
    assert players.brayden_risedorph.group == "IU Player/Alumni"