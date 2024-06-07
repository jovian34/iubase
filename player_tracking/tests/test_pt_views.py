import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import date, datetime

from player_tracking.tests.fixtures import players, transactions, annual_rosters
from live_game_blog.tests.fixtures import teams

from accounts.models import CustomUser
from accounts.tests.fixtures import user_not_logged_in, user_iubase17, logged_user_schwarbs

@pytest.mark.django_db
def test_index(client, players):
    response = client.get(reverse("players"))
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_add_player_form_renders(client, logged_user_schwarbs):
    response = client.get(reverse("add_player"))
    assert response.status_code == 200
    assert "First Name" in str(response.content)
    assert "Headshot or other photo file URL" in str(response.content)


@pytest.mark.django_db
def test_add_player_form_redirects_not_logged_in(client):
    response = client.get(reverse("add_player"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_player_form_adds_new_player(client, players, logged_user_schwarbs):
    response = client.post(
        reverse("add_player"),
        {
            "first": ["Phillip"],
            "last": ["Glasser"],
            "hsgrad_year": ["2018"],
            "high_school": ["Tallmadge"],
            "home_city": ["Tallmadge"],
            "home_state": ["OH"],
            "home_country": ["USA"],
            "headshot": ["https://www.prepbaseballreport.com/passets/photo/OH/8542307196-PhillipGlasser.png"],
            "birthdate": ["1999-12-03"],
            "bats": ["Left"],
            "throws": ["Right"],
            "height": [72],
            "weight": [170],
            "trans_event": ["Verbal Commitment from College"],
            "trans_date": ["2021-06-15"],
            "primary_position": ["Shortstop"],
            "citation": ["https://d1baseball.com/transfers/2021-22-d1baseball-transfer-tracker/"]
        },
        follow=True,                      
    )
    assert response.status_code == 200
    assert "Phillip Glasser rosters" in str(response.content)
    assert "Verbal Commitment from College" in str(response.content)
    assert "June 15, 2021:" in str(response.content)


@pytest.mark.django_db
def test_add_player_form_asks_for_password_not_logged_in(client, players):
    response = client.post(
        reverse("add_player"),
        {
            "first": ["Phillip"],
            "last": ["Glasser"],
            "hsgrad_year": ["2018"],
            "high_school": ["Tallmadge"],
            "home_city": ["Tallmadge"],
            "home_state": ["OH"],
            "home_country": ["USA"],
            "headshot": ["https://www.prepbaseballreport.com/passets/photo/OH/8542307196-PhillipGlasser.png"],
            "birthdate": ["1999-12-03"],
            "bats": ["Left"],
            "throws": ["Right"],
            "height": [72],
            "weight": [170],
            "clock": [5],
        },
        follow=True,                      
    )
    assert response.status_code == 200
    assert "Password" in str(response.content)



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
def test_add_roster_year_partial_get_renders_form_fields(client, players, teams, logged_user_schwarbs):
    response = client.get(reverse(
        "add_roster_year",
        args=[players.nm2021.pk],
    ))
    assert response.status_code == 200
    assert "Spring Year" in str(response.content)
    assert "Indiana" in str(response.content)
    assert str(timezone.now().year) in str(response.content)


@pytest.mark.django_db
def test_add_transaction_partial_get_renders_form_fields(client, players, teams, logged_user_schwarbs):
    response = client.get(reverse(
        "add_transaction",
        args=[players.nm2021.pk],
    ))
    assert response.status_code == 200
    assert "Transaction Event" in str(response.content)
    assert "Transaction Date" in str(response.content)
    assert str(timezone.now().year) in str(response.content)


@pytest.mark.django_db
def test_add_roster_year_partial_get_redirects_not_logged_in(client, players, teams):
    response = client.get(reverse(
        "add_roster_year",
        args=[players.nm2021.pk],
    ))
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_transaction_partial_get_redirects_not_logged_in(client, players, teams):
    response = client.get(reverse(
        "add_transaction",
        args=[players.nm2021.pk],
    ))
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_roster_year_partial_post_adds_roster_year(client, players, teams, annual_rosters, logged_user_schwarbs):
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


@pytest.mark.django_db
def test_add_transaction_partial_post_adds_transaction(client, players, teams, annual_rosters, logged_user_schwarbs):
    response = client.post(
        reverse("add_transaction", args=[players.nm2021.pk]),
        {
            "trans_event": ["Drafted"],
            "trans_date": [str(date(2024, 7, 17))],
            "citation": ["https://www.mlb.com/draft/tracker"],
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Drafted" in str(response.content)
    assert "July 17" in str(response.content)
    assert 'href="https://www.mlb.com/draft/tracker"'


@pytest.mark.django_db
def test_add_roster_year_partial_post_asks_for_password_not_logged_in(client, players, teams, annual_rosters):
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
    assert "Password" in str(response.content)


def test_pt_index_renders(client):
    response = client.get(reverse("pt_index"))
    assert response.status_code == 200
    assert f"{str(timezone.now().year)} Depth Chart" in str(response.content)


@pytest.mark.django_db
def test_fall_depth_chart_renders(client, players, teams, annual_rosters):
    response = client.get(reverse("fall_depth_chart", args=["2023"]))
    assert response.status_code == 200
    assert "Corner Outfield" in str(response.content)
    assert "Fall 2023 Available Depth Chart" in str(response.content)
    assert "Devin Taylor" in str(response.content)
    assert "Brayden" not in str(response.content)

@pytest.mark.django_db
def test_spring_depth_chart_renders(client, players, teams, annual_rosters):
    response = client.get(reverse("spring_depth_chart", args=["2023"]))
    assert response.status_code == 200
    assert "Catcher" in str(response.context)
    assert "Spring 2023 Available Depth Chart" in str(response.content)
    assert "Devin Taylor" in str(response.content)
    assert "Nick" not in str(response.content) # on different team


@pytest.mark.django_db
def test_fall_roster_renders(client, players, teams, annual_rosters):
    response = client.get(reverse("fall_roster", args=["2023"]))
    print(response.content)
    assert response.status_code == 200
    assert "Total Roster Length: 2" in str(response.content)
    assert "Fall 2023 Roster" in str(response.content)
    assert "Nick Mitchell" in str(response.content)
    assert "Brayden" not in str(response.content)


@pytest.mark.django_db
def test_spring_roster_renders(client, players, teams, annual_rosters):
    response = client.get(reverse("spring_roster", args=["2023"]))
    assert response.status_code == 200
    assert "Total Roster Length: 2" in str(response.content)
    assert "Spring 2023 Roster" in str(response.content)
    assert "Nick Mitchell" not in str(response.content)
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_portal_page_renders(client, players, teams, annual_rosters, transactions):
    current_dt = datetime.now()
    response = client.get(reverse("portal", args=[str(current_dt.year)]))
    assert response.status_code == 200
    assert "Total Players in the Portal: 1"
    assert "Brooks" in str(response.content)
    assert "Brooks Ey" in str(response.content)
    assert "Devin" not in str(response.content)


@pytest.mark.django_db
def test_set_last_spring_produces_correct_values(client, players, annual_rosters, transactions, logged_user_schwarbs):
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    assert "Devin Taylor 2023-2026" in str(response.content)
    assert "Brooks Ey 2022-2024" in str(response.content)