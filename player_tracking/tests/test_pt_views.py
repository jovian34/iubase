import pytest
from django.urls import reverse
from django.utils import timezone

from player_tracking.tests.fixtures import players, transactions, annual_rosters
from live_game_blog.tests.fixtures import teams


@pytest.mark.django_db
def test_index(client, players):
    response = client.get(reverse("players"))
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_player_rosters_renders_one_player_only(client, annual_rosters):
    response = client.get(reverse(
        "player_rosters",
        args=[annual_rosters.dt_2023.player.pk],
    ))
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)
    assert "Nick" not in str(response.content)


@pytest.mark.django_db
def test_player_rosters_renders_transfer_player_old_team(client, annual_rosters):
    response = client.get(reverse(
        "player_rosters",
        args=[annual_rosters.nm_2023.player.pk],
    ))
    assert response.status_code == 200
    assert "Nick Mitchell" in str(response.content)
    assert "Devin" not in str(response.content)
    assert "Miami (Ohio)" in str(response.content)


@pytest.mark.django_db
def test_add_roster_year_partial_get_renders_form_fields(client, players, teams):
    response = client.get(reverse(
        "add_roster_year",
        args=[players.nm2021.pk],
    ))
    assert response.status_code == 200
    assert "Spring Year" in str(response.content)
    assert "Indiana" in str(response.content)
    assert str(timezone.now().year) in str(response.content)


@pytest.mark.django_db
def test_add_roster_year_partial_post_adds_roster_year(client, players, teams, annual_rosters):
    response = client.post(
        reverse("add_roster_year", args=[players.nm2021.pk]),
        {
            "spring_year": [2022],
            "team": [str(teams.duke.pk)],
            "jersey": [29],
            "status": ["Spring Roster"],
            "primary_position": ["Centerfield"],
            "secondary_position": [],
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "2024 Indiana" in str(response.content)
    assert "2023 Miami (Ohio)" in str(response.content)
    assert "2022 Duke" in str(response.content)