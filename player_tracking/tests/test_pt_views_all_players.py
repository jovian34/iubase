import pytest
from django.urls import reverse


from player_tracking.tests.fixtures.players import players


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