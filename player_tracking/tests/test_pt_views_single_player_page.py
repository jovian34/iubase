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
from player_tracking.tests.fixtures.accolades import accolades
from live_game_blog.tests.fixtures.teams import teams
from accounts.tests.fixtures import logged_user_schwarbs


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
    assert "Devin Taylor" in response.content.decode()
    assert "Nick" not in response.content.decode()


@pytest.mark.django_db
def test_single_player_page_raises_404_if_not_in_database(
    client, players, annual_rosters
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[5748454752],
        )
    )
    assert response.status_code == 404


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
    assert "Devin Taylor" in response.content.decode()
    assert "Summer Ball:" in response.content.decode()
    assert (
        f"{this_year}: USA Collegiate National Team of the International Friendship League"
        in response.content.decode()
    )


@pytest.mark.django_db
def test_single_player_page_renders_transfer_player_old_team(
    client, annual_rosters, players
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.nick_mitchell.pk],
        )
    )
    assert response.status_code == 200
    assert "Nick Mitchell" in response.content.decode()
    assert "Devin" not in response.content.decode()
    assert "Miami (Ohio)" in response.content.decode()


@pytest.mark.django_db
def test_single_player_page_renders_action_shot_for_that_player(
    client, players, annual_rosters
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert "https://live.staticflickr.com/65535/54014518896_5c58571da6_o.jpg" in str(
        response.content
    )
    assert (
        "https://iubase.com/wp-content/uploads/2024/11/53704071552_13227a46a0_k.jpg"
        not in response.content.decode()
    )


@pytest.mark.django_db
def test_single_player_page_renders_generic_action_shot_if_one_does_not_exist(
    client, players, annual_rosters
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.brayden_risedorph.pk],
        )
    )
    assert (
        "https://iubase.com/wp-content/uploads/2024/11/53704071552_13227a46a0_k.jpg"
        in response.content.decode()
    )


@pytest.mark.django_db
def test_single_player_page_renders_accolade_org_and_name(
    client, players, annual_rosters, accolades
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in response.content.decode()


@pytest.mark.django_db
def test_single_player_page_omits_add_and_edit_buttons_not_logged_in(
    client, players, annual_rosters
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in response.content.decode()
    assert "add accolade</button>" not in response.content.decode()
    assert "add summer assignment</button>" not in response.content.decode()
    assert "add transaction</button>" not in response.content.decode()
    assert "add roster year</button>"not  in response.content.decode()
    assert "edit player info</button>" not in response.content.decode()
    assert "B1G First Team All-Conference Outfielder" not in response.content.decode()


@pytest.mark.django_db
def test_single_player_page_omits_add_and_edit_buttons_without_perms(
    client, players, annual_rosters, logged_user_schwarbs
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in response.content.decode()
    assert "add accolade</button>" not in response.content.decode()
    assert "add summer assignment</button>" not in response.content.decode()
    assert "add transaction</button>" not in response.content.decode()
    assert "add roster year</button>"not  in response.content.decode()
    assert "edit player info</button>" not in response.content.decode()
    assert "B1G First Team All-Conference Outfielder" not in response.content.decode()


@pytest.mark.django_db
def test_single_player_page_renders_add_and_edit_buttons_with_perms(
    admin_client, players, annual_rosters,
):
    response = admin_client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in response.content.decode()
    assert "add accolade</button>" in response.content.decode()
    assert "add summer assignment</button>" in response.content.decode()
    assert "add transaction</button>" in response.content.decode()
    assert "add roster year</button>" in response.content.decode()
    assert "edit player info</button>" in response.content.decode()


@pytest.mark.django_db
def test_single_player_page_renders_accolades_in_reverse_date_order(
    client, players, annual_rosters, accolades
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.devin_taylor.pk],
        )
    )
    assert response.status_code == 200
    pre = response.content.decode().find("Pre-season second team All-American Outfielder")
    first = response.content.decode().find("First Team All-Conference")
    sec = response.content.decode().find("2nd team All-American Outfielder")
    assert sec < first
    assert first < pre


@pytest.mark.django_db
def test_single_player_page_renders_summer_accolades_after_summer_header(
    client,
    players,
    annual_rosters,
    accolades,
    summer_assign,
    summer_leagues,
    summer_teams,
):
    response = client.get(
        reverse(
            "single_player_page",
            args=[players.ryan_kraft.pk],
        )
    )
    assert response.status_code == 200
    assert "Ryan Kraft" in response.content.decode()
    assert "Northwoods League Pitcher of the Year" in response.content.decode()
    other = response.content.decode().find("Other Accolades:")
    head = response.content.decode().find("Summer Ball:")
    award = response.content.decode().find("Northwoods League Pitcher of the Year")
    assert head < award
    assert award < other
