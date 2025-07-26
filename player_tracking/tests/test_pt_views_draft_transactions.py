import pytest
from django import urls

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from live_game_blog.tests.fixtures.teams import teams


@pytest.mark.xfail
@pytest.mark.django_db
def test_group_draft_transactions_render(client):
    response = client.get(urls.reverse("draft_transactions"))
    assert response.status_code == 200


@pytest.mark.xfail
@pytest.mark.django_db
def test_group_draft_transactions_shows_title(client, transactions, players):
    response = client.get(urls.reverse("draft_transactions"))
    assert "All Draft and Signing Transactions" in str(response.content)


@pytest.mark.xfail
@pytest.mark.django_db
def test_group_draft_transactions_list_player(client, transactions, players):
    response = client.get(urls.reverse("draft_transactions"))
    assert "Nick Mitchell, Drafted" in str(response.content)


@pytest.mark.xfail
@pytest.mark.django_db
def test_group_draft_transactions_reverse_chron_order(client, transactions, players):
    response = client.get(urls.reverse("draft_transactions"))
    output = str(response.content)
    nm = output.find("Nick Mitchell, Drafted")
    gh = output.find("Grant Hollister, Drafted")
    assert nm < gh