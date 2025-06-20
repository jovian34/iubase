import pytest
from django.urls import reverse
from datetime import date

from live_game_blog.tests.fixtures.teams import teams
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.tests.fixtures.prof_org import prof_orgs


this_year = date.today().year
last_year = this_year - 1


@pytest.mark.django_db
def test_portal_page_renders(client, players, teams, annual_rosters, transactions):
    response = client.get(reverse("portal", args=[str(this_year)]))
    assert response.status_code == 200
    assert "Total Players in the Portal: 1"
    assert "Brooks Ey" in str(response.content)
    assert "Devin" not in str(response.content)


@pytest.mark.django_db
def test_portal_page_shows_date_entered(
    client, players, teams, annual_rosters, transactions
):
    response = client.get(reverse("portal", args=[str(this_year)]))
    assert response.status_code == 200
    assert f"Entered the portal</a> on June 15, {str(this_year)}" in str(
        response.content
    )


@pytest.mark.django_db
def test_portal_page_links_to_citation(
    client, players, teams, annual_rosters, transactions
):
    response = client.get(reverse("portal", args=[str(this_year)]))
    assert response.status_code == 200
    assert '<a href="https://x.com/brooks_ey/status/1794162572117303480">' in str(
        response.content
    )


@pytest.mark.django_db
def test_portal_page_shows_date_commited(
    client, players, teams, annual_rosters, transactions
):
    response = client.get(reverse("portal", args=[str(last_year)]))
    assert response.status_code == 200
    assert f"From the portal</a> on July 15, {str(last_year)}" in str(response.content)


@pytest.mark.django_db
def test_portal_page_shows_outgoing_commit_school(
    client, players, teams, annual_rosters, transactions
):
    response = client.get(reverse("portal", args=[str(this_year)]))
    assert response.status_code == 200
    assert "Committed to Duke" in str(response.content)
