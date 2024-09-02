import pytest
from django.urls import reverse
from datetime import date, datetime

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
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
from accounts.tests.fixtures import logged_user_schwarbs


this_year = date.today().year


@pytest.mark.django_db
def test_all_players_renders(client, players):
    response = client.get(reverse("players"))
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_all_players_renders_in_alpha_order_by_last_name(client, players):
    response = client.get(reverse("players"))
    assert response.status_code == 200
    output = str(response.content)
    nb = output.find("Nate Ball")
    br = output.find("Brayden Risedorph")
    assert br > nb


@pytest.mark.django_db
def test_all_players_renders_in_alpha_order_by_case_insensitive_last_name(
    client, players
):
    """
    Edge case where player's last name starts with a lower case letter
    The order_by function normally orders capital letters before lower case
    a Lower() method is applied to make the ordering case insensative
    """
    response = client.get(reverse("players"))
    assert response.status_code == 200
    output = str(response.content)
    oo = output.find("Owen ten Oever")
    aw = output.find("Andrew Wiggins")
    assert aw > oo


@pytest.mark.django_db
def test_player_rosters_renders_one_player_only(client, annual_rosters):
    response = client.get(
        reverse(
            "player_rosters",
            args=[annual_rosters.dt_fresh.player.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)
    assert "Nick" not in str(response.content)


@pytest.mark.django_db
def test_player_rosters_renders_summer_teams(
    client, annual_rosters, summer_assign, summer_leagues, summer_teams
):
    response = client.get(
        reverse(
            "player_rosters",
            args=[annual_rosters.dt_fresh.player.pk],
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
def test_player_rosters_renders_transfer_player_old_team(client, annual_rosters):
    response = client.get(
        reverse(
            "player_rosters",
            args=[annual_rosters.nm_soph.player.pk],
        )
    )
    assert response.status_code == 200
    assert "Nick Mitchell" in str(response.content)
    assert "Devin" not in str(response.content)
    assert "Miami (Ohio)" in str(response.content)


@pytest.mark.django_db
def test_pt_index_renders(client):
    response = client.get(reverse("pt_index"))
    assert response.status_code == 200
    assert f"{this_year} Depth Chart" in str(response.content)


@pytest.mark.django_db
def test_fall_roster_renders(client, players, teams, annual_rosters):
    response = client.get(reverse("fall_roster", args=[f"{this_year - 1}"]))
    assert response.status_code == 200
    assert "Total Roster Length: 4" in str(response.content)
    assert f"Fall {this_year - 1} Roster" in str(response.content)
    assert "Nathan Ball" in str(response.content)
    assert "Nick Mitchell" in str(response.content)
    assert "Jack Moffitt" in str(response.content)
    assert "Brayden" not in str(response.content)


@pytest.mark.django_db
def test_fall_roster_fw_to_instead_of_projection(
    client, players, teams, annual_rosters
):
    response = client.get(reverse("projected_players_fall", args=[f"{this_year - 1}"]))
    assert response.status_code == 302
    response = client.get(
        reverse("projected_players_fall", args=[f"{this_year - 1}"]), follow=True
    )
    assert response.status_code == 200
    assert "Total Roster Length: 4" in str(response.content)
    assert f"Fall {this_year - 1} Roster" in str(response.content)
    assert "Nathan Ball" in str(response.content)
    assert "Nick Mitchell" in str(response.content)
    assert "Jack Moffitt" in str(response.content)
    assert "Brayden" not in str(response.content)


@pytest.mark.django_db
def test_spring_roster_renders(client, players, teams, annual_rosters):
    response = client.get(reverse("spring_roster", args=[f"{this_year - 1}"]))
    assert response.status_code == 200
    assert "Total Roster Length: 2" in str(response.content)
    assert f"Spring {this_year - 1} Roster" in str(response.content)
    assert "Nick Mitchell" not in str(response.content)
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_summer_assignments_page_renders(
    client, players, summer_assign, summer_leagues, summer_teams
):
    response = client.get(reverse("summer_assignments", args=[f"{this_year}"]))
    assert response.status_code == 200
