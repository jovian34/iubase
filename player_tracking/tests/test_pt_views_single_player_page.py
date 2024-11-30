import pytest
from django.urls import reverse
from datetime import date

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.mlb_draft_date import typical_mlb_draft_date
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.tests.fixtures.summer import (
    summer_assign,
    summer_leagues,
    summer_teams,
)
from live_game_blog.tests.fixtures.teams import teams


this_year = date.today().year


@pytest.mark.django_db
def test_single_player_page_renders_one_player_only(client, players, annual_rosters):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)
    assert "Nick" not in str(response.content)


@pytest.mark.django_db
def test_single_player_page_renders_summer_teams(
    client, players, annual_rosters, summer_assign, summer_leagues, summer_teams
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)
    assert "Summer Ball:" in str(response.content)
    assert (
        f"{this_year}: USA Collegiate National Team of the International Friendship League"
        in str(response.content)
    )


@pytest.mark.django_db
def test_single_player_page_renders_transfer_player_old_team(client, annual_rosters, players):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.nick_mitchell.pk],
        )
    )
    assert response.status_code == 200
    assert "Nick Mitchell" in str(response.content)
    assert "Devin" not in str(response.content)
    assert "Miami (Ohio)" in str(response.content)


@pytest.mark.django_db
def test_single_player_page_renders_action_shot_for_that_player(client, players, annual_rosters):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert "https://live.staticflickr.com/65535/54014518896_5c58571da6_o.jpg" in str(response.content)
    assert "https://iubase.com/wp-content/uploads/2024/11/53704071552_13227a46a0_k.jpg" not in str(response.content)


@pytest.mark.django_db
def test_single_player_page_renders_generic_action_shot_if_one_does_not_exist(client, players, annual_rosters):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.brayden_risedorph.pk],
        )
    )
    assert "https://iubase.com/wp-content/uploads/2024/11/53704071552_13227a46a0_k.jpg" in str(response.content)