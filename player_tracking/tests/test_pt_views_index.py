import pytest
from django.urls import reverse
from datetime import date

from accounts.tests.fixtures import logged_user_schwarbs


this_year = date.today().year


@pytest.mark.django_db
def test_pt_index_renders(client):
    response = client.get(reverse("pt_index"))
    assert response.status_code == 200
    assert f"{this_year} Roster Not Yet Announced" in response.content.decode()
    assert f"{this_year} Depth Chart" in response.content.decode()


@pytest.mark.django_db
def test_pt_index_renders_add_player_if_perms(admin_client):
    response = admin_client.get(reverse("pt_index"))
    assert response.status_code == 200
    assert "Add Player" in response.content.decode()


@pytest.mark.django_db
def test_pt_index_no_add_player_if_not_logged_in(client):
    response = client.get(reverse("pt_index"))
    assert response.status_code == 200
    assert "Add Player" not in response.content.decode()


@pytest.mark.django_db
def test_pt_index_no_add_player_if_not_permitted(client, logged_user_schwarbs):
    response = client.get(reverse("pt_index"))
    assert response.status_code == 200
    assert "Add Player" not in response.content.decode()
