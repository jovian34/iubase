import pytest
from django.urls import reverse

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