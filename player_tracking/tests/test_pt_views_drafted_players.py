import pytest
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.mlb_draft_date import mlb_draft_date
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.views.drafted_players import group_drafted_player

from live_game_blog.tests.fixtures.teams import teams


this_year = date.today().year


@pytest.mark.django_db
def test_group_drafted_player_groups_high_school(players):
    group_drafted_player(draft_year=f"{this_year}", player=players.grant_hollister)
    assert players.grant_hollister.group == "High School Signee"


@pytest.mark.django_db
def test_group_drafted_player_groups_iu(players):
    group_drafted_player(draft_year=f"{this_year}", player=players.brayden_risedorph)
    assert players.brayden_risedorph.group == "IU Player/Alumni"


@pytest.mark.django_db
def test_drafted_players_renders_drafted_not_signed(
    client, players, prof_orgs, transactions, annual_rosters, mlb_draft_date
):
    response = client.get(reverse("drafted_players", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert "Grant Hollister" in str(response.content)
    assert response.context["count"] == 2
    assert "High School Signee" in str(response.content)
    assert "IU Player/Alumni" in str(response.content)
    assert "He is expected by insiders to require $500,000 to sign." in str(
        response.content
    )
    assert "$400,100 before" not in str(response.content)
    assert "Philadelphia Phillies incur" not in str(response.content)


@pytest.mark.django_db
def test_drafted_players_renders_signed(
    client, players, prof_orgs, transactions, annual_rosters, mlb_draft_date
):
    response = client.get(reverse("drafted_players", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert response.context["count"] == 2
    assert (
        "Nick Mitchell signed a professional contract with a bonus of $367,000."
        in str(response.content)
    )
    assert "This bonus was 92% of the assigned value of the draft pick." in str(
        response.content
    )
    assert "Bonus value was reported two days after signing." in str(response.content)


@pytest.mark.django_db
def test_drafted_players_renders_unsigned(
    client, players, prof_orgs, transactions, annual_rosters, mlb_draft_date
):
    response = client.get(reverse("drafted_players", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert "Grant Hollister did not sign and will be on campus in the fall." in str(
        response.content
    )
