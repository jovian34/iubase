import pytest
from datetime import date

from player_tracking.tests.fixtures.players import players
from player_tracking.views.visitor_logic import group_drafted_player


this_year = date.today().year


@pytest.mark.django_db
def test_group_drafted_player_groups_high_school(players):
    group_drafted_player(draft_year=f"{this_year}", player=players.grant_hollister)
    assert players.grant_hollister.group == "High School Signee"


@pytest.mark.django_db
def test_group_drafted_player_groups_iu(players):
    group_drafted_player(draft_year=f"{this_year}", player=players.brayden_risedorph)
    assert players.brayden_risedorph.group == "IU Player/Alumni"