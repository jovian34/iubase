import pytest
from django.urls import reverse
from datetime import date
from unittest.mock import Mock

from accounts.tests.fixtures import logged_user_schwarbs
from live_game_blog.tests.fixtures.teams import teams
from player_tracking.models import AnnualRoster
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.players import players


this_year = date.today().year


@pytest.mark.django_db
def test_pt_index_renders_november_through_june_sections(client, monkeypatch):
    monkeypatch.setattr(
        "player_tracking.views.pt_index.date",
        Mock(today=Mock(return_value=date(this_year, 11, 15))),
    )
    response = client.get(reverse("pt_index"))
    assert response.status_code == 200
    assert f"Spring {this_year + 1} Team" in response.content.decode()
    assert f"Fall {this_year + 1} Team" in response.content.decode()
    assert "All Players in the database" in response.content.decode()


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


@pytest.mark.django_db
def test_pt_index_renders_current_red_belt_entry_link_if_permitted(
    admin_client, monkeypatch
):
    monkeypatch.setattr(
        "player_tracking.views.pt_index.date",
        Mock(today=Mock(return_value=date(this_year, 11, 15))),
    )
    response = admin_client.get(reverse("pt_index"))
    red_belt_entry_url = reverse("red_belt_entry", args=[this_year])
    assert response.status_code == 200
    assert f'href="{red_belt_entry_url}"' in response.content.decode()


@pytest.mark.django_db
def test_pt_index_hides_red_belt_entry_link_without_permission(
    client, logged_user_schwarbs
):
    response = client.get(reverse("pt_index"))
    red_belt_entry_url = reverse("red_belt_entry", args=[this_year])
    assert response.status_code == 200
    assert f'href="{red_belt_entry_url}"' not in response.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize("month", [7, 8, 9, 10])
def test_pt_index_uses_current_template_from_july_through_october(
    client, monkeypatch, month
):
    monkeypatch.setattr(
        "player_tracking.views.pt_index.date",
        Mock(today=Mock(return_value=date(2026, month, 15))),
    )

    response = client.get(reverse("pt_index"))

    assert response.status_code == 200
    assert "player_tracking/pt_index_jul_oct.html" in [
        template.name for template in response.templates
    ]


@pytest.mark.django_db
@pytest.mark.parametrize("month", [11, 12, 1, 2, 3, 4, 5, 6])
def test_pt_index_uses_november_through_june_template(client, monkeypatch, month):
    year = 2026 if month >= 11 else 2027
    monkeypatch.setattr(
        "player_tracking.views.pt_index.date",
        Mock(today=Mock(return_value=date(year, month, 15))),
    )

    response = client.get(reverse("pt_index"))

    assert response.status_code == 200
    assert "player_tracking/pt_index_nov_jun.html" in [
        template.name for template in response.templates
    ]


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("month", "year"),
    [(11, 2027), (12, 2027), (1, 2026), (2, 2026), (3, 2026), (4, 2026), (5, 2026), (6, 2026)],
)
def test_pt_index_nov_jun_shows_spring_and_fall_teams_for_season_year(
    client, monkeypatch, month, year
):
    calendar_year = year - 1 if month in [11, 12] else year
    monkeypatch.setattr(
        "player_tracking.views.pt_index.date",
        Mock(today=Mock(return_value=date(calendar_year, month, 15))),
    )

    response = client.get(reverse("pt_index"))
    content = response.content.decode()
    spring_portal_url = reverse("portal", args=[year - 1])
    fall_portal_url = reverse("portal", args=[year])
    incoming_players_url = reverse("incoming_players", args=[year])
    spring_team_index = content.index(f"Spring {year} Team")
    spring_last_link_index = content.index(
        f"Spring {year} Red Belt Leaderboard"
    )
    fall_team_index = content.index(f"Fall {year} Team")
    fall_roster_index = content.index(f"Fall {year} Roster")
    draft_section_index = content.index("<h2>MLB Draft</h2>")
    spring_portal_index = content.index(f"Transfer Portal {year - 1}")
    fall_portal_index = content.index(f"Transfer Portal {year}")
    incoming_players_index = content.index(f"Incoming Players For Fall {year}")

    assert response.status_code == 200
    assert f"Spring {year} Team" in content
    assert f"Fall {year} Team" in content
    assert f'href="{spring_portal_url}"' in content
    assert f'href="{fall_portal_url}"' in content
    assert f'href="{incoming_players_url}"' in content
    assert spring_team_index < spring_last_link_index < spring_portal_index < fall_team_index
    assert fall_team_index < incoming_players_index < fall_portal_index
    assert fall_team_index < fall_roster_index < fall_portal_index < draft_section_index
    assert "All Players in the database" in content


@pytest.mark.django_db
@pytest.mark.parametrize("month", [8, 11])
def test_pt_index_has_separate_mlb_draft_section_before_all_players(
    client, monkeypatch, month
):
    monkeypatch.setattr(
        "player_tracking.views.pt_index.date",
        Mock(today=Mock(return_value=date(2026, month, 15))),
    )

    response = client.get(reverse("pt_index"))
    content = response.content.decode()

    draft_section_index = content.index("<h2>MLB Draft</h2>")
    drafted_players_index = content.index("Players Selected in the 2026 MLB Draft")
    draft_transactions_index = content.index(
        "All MLB Draft and Pro Signing Transactions"
    )
    all_players_index = content.index("All Players in the database")

    assert response.status_code == 200
    assert draft_section_index < drafted_players_index < all_players_index
    assert draft_section_index < draft_transactions_index < all_players_index


@pytest.mark.django_db
def test_pt_index_links_to_previous_fall_roster_until_spring_roster_exists(
    client, monkeypatch, annual_rosters, players, teams
):
    current_year = date.today().year
    spring_year = current_year + 1
    monkeypatch.setattr(
        "player_tracking.views.pt_index.date",
        Mock(today=Mock(return_value=date(current_year, 11, 15))),
    )

    AnnualRoster.objects.create(
        spring_year=spring_year,
        status="Fall Roster",
        player=players.jake_stadler,
        team=teams.indiana,
        jersey=9,
        primary_position="Catcher",
    )

    response = client.get(reverse("pt_index"))
    fall_roster_url = reverse("fall_roster", args=[current_year])
    spring_depth_chart_url = reverse("spring_depth_chart", args=[spring_year])
    content = response.content.decode()

    assert response.status_code == 200
    assert f'href="{fall_roster_url}"' in content
    assert f'href="{spring_depth_chart_url}"' not in content


@pytest.mark.django_db
def test_pt_index_links_to_spring_roster_after_first_spring_player(
    client, monkeypatch, annual_rosters, players, teams
):
    current_year = date.today().year
    spring_year = current_year + 1
    monkeypatch.setattr(
        "player_tracking.views.pt_index.date",
        Mock(today=Mock(return_value=date(current_year, 11, 15))),
    )

    AnnualRoster.objects.create(
        spring_year=spring_year,
        status="Spring Roster",
        player=players.jake_stadler,
        team=teams.indiana,
        jersey=9,
        primary_position="Catcher",
    )

    response = client.get(reverse("pt_index"))
    spring_roster_url = reverse("spring_roster", args=[spring_year])
    spring_depth_chart_url = reverse("spring_depth_chart", args=[spring_year])
    fall_roster_url = reverse("fall_roster", args=[current_year])
    content = response.content.decode()

    assert response.status_code == 200
    assert f'href="{spring_roster_url}"' in content
    assert f'href="{spring_depth_chart_url}"' in content
    assert f'href="{fall_roster_url}"' not in content
