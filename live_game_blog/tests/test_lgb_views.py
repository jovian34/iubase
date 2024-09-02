import pytest

from datetime import datetime, timedelta
from django.urls import reverse

from live_game_blog.tests.fixtures.fixtures import (
    teams,
    games,
    scoreboard,
    logged_user_schwarbs,
    blog_entries,
    user_not_logged_in,
    user_iubase17,
)


@pytest.mark.django_db
def test_games_list_page_renders_road_and_neutral_future(client, teams, games):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "Indiana" in str(response.content)
    assert "versus" in str(response.content)
    assert "at" in str(response.content)


@pytest.mark.django_db
def test_games_list_page_does_not_render_canc_games(client, teams, games, scoreboard):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "Coastal Carolina" in str(response.content)
    assert "Miami" not in str(response.content)


@pytest.mark.django_db
def test_games_list_page_does_not_render_past_games(client, teams, games, scoreboard):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "Coastal Carolina" in str(response.content)
    assert "Kentucky" not in str(response.content)


@pytest.mark.django_db
def test_games_list_page_does_not_render_four_games_out(
    client, teams, games, scoreboard
):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "George Mason" in str(response.content)
    assert "Miami" not in str(response.content)


@pytest.mark.django_db
def test_games_list_page_renders_logo(client, teams, games):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert f"cdn.d1baseball" in str(response.content)


@pytest.mark.django_db
def test_past_game_renders_partial_with_score(client, teams, games, scoreboard):
    response = client.get(reverse("past_games"))
    assert response.status_code == 200
    assert "Kentucky-4" in str(response.content)


@pytest.mark.django_db
def test_live_single_game_blog_page_renders(client, games, scoreboard, blog_entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    assert "Joey" in str(response.content)
    assert "Indiana at Kentucky," in str(response.content)
    assert "(FINAL)" in str(response.content)
    assert "Kentucky moves on to Super Regionals" in str(response.content)


@pytest.mark.django_db
def test_edit_live_single_game_blog_page_renders(
    client, games, scoreboard, blog_entries, logged_user_schwarbs
):
    response = client.get(reverse("edit_live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_live_single_game_blog_page_redirects_not_logged_in(
    client, games, scoreboard, blog_entries
):
    response = client.get(reverse("edit_live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_blog_entry_plus_scoreboard_form(client, logged_user_schwarbs, games):
    response = client.post(
        reverse("add_blog_plus_scoreboard", args=[games.iu_duke.pk]),
        {
            "game_status": "in-progress",
            "inning_num": "2",
            "inning_part": "Bottom",
            "outs": "3",
            "home_runs": "1",
            "away_runs": "3",
            "home_hits": "2",
            "away_hits": "5",
            "home_errors": "1",
            "away_errors": "0",
            "blog_entry": "Indiana holds Duke to one run",
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Indiana holds Duke to one run" in str(response.content)
    assert "Kyle" in str(response.content)
    assert "End of bottom of inning 2" in str(response.content)


@pytest.mark.django_db
def test_add_blog_entry_only_post_form(client, logged_user_schwarbs, games, scoreboard):
    response = client.post(
        reverse("add_blog_entry_only", args=[games.iu_duke.pk]),
        {
            "blog_entry": "Adding to the Duke Blog",
            "is_x_embed": False,
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Adding to the Duke Blog" in str(response.content)
    assert "Kyle" in str(response.content)


@pytest.mark.django_db
def test_add_blog_entry_only_x_embed_post_form(
    client, logged_user_schwarbs, user_iubase17, games, scoreboard
):
    response = client.post(
        reverse("add_blog_entry_only", args=[games.iu_duke.pk]),
        {
            "blog_entry": "<li>Adding to the Duke Blog",
            "is_raw_html": True,
            "is_x_embed": True,
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "<li>Adding to the Duke Blog" in str(response.content)
    assert "entry by @iubase17" in str(response.content)


@pytest.mark.django_db
def test_edit_blog_entry_adds_text(client, logged_user_schwarbs, games, blog_entries):
    response = client.post(
        reverse("edit_blog_entry", args=[blog_entries.blog_uk_mon_y.pk]),
        {
            "blog_entry": "Ty had a great 2nd inning",
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Bothwell walks the first batter" not in str(response.content)
    assert "Ty had a great 2nd inning" in str(response.content)


@pytest.mark.django_db
def test_edit_blog_entry_changes_hit_to_error(
    client, logged_user_schwarbs, games, blog_entries
):
    response = client.post(
        reverse("edit_blog_entry", args=[blog_entries.blog_uk_mon_z.pk]),
        {
            "blog_entry": "Kentucky moves on to Super Regionals",
            "game_status": "final",
            "inning_num": "9",
            "inning_part": "Top",
            "outs": "3",
            "home_runs": "4",
            "away_runs": "2",
            "home_hits": "7",
            "away_hits": "10",
            "home_errors": "1",
            "away_errors": "2",
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "8 hits" not in str(response.content)
    assert "2 errors" in str(response.content)


@pytest.mark.django_db
def test_add_game_page_renders(client, logged_user_schwarbs):
    response = client.get(reverse("add_game"))
    assert response.status_code == 200
    assert "Is this a neutral site or host is designated away?" in str(response.content)
    assert "Away team D1Baseball.com national ranking" in str(response.content)
    assert "Away team national tournament seed" in str(response.content)
    assert "Home team tournament seed" in str(response.content)
    assert "Live Stats Link" in str(response.content)
    assert "Video Stream or TV provider" in str(response.content)
    assert "Student Audio Link" in str(response.content)
    assert "Date and Time of First Pitch YYYY-MM-DD-HHMM in ET military time" in str(
        response.content
    )
    assert "Primary Audio Link" in str(response.content)


@pytest.mark.django_db
def test_add_game(client, logged_user_schwarbs, teams, games, scoreboard):
    response = client.post(
        reverse("add_game"),
        {
            "home_team": [str(teams.indiana.pk)],
            "away_team": [str(teams.gm.pk)],
            "neutral_site": ["on"],
            "live_stats": [
                "https://stats.statbroadcast.com/broadcast/?id=491945&vislive=ind"
            ],
            "first_pitch": ["2025-02-14-1830"],
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Feb. 14, 2025, 6:30 p.m. first pitch" in str(response.content)
    assert "Scoreboard: George Mason-0, Indiana-0 | Top Inning: 1" in str(
        response.context
    )


@pytest.mark.django_db
def test_add_tourney_game(client, logged_user_schwarbs, teams, games, scoreboard):
    response = client.post(
        reverse("add_game"),
        {
            "home_team": [str(teams.kentucky.pk)],
            "home_rank": ["20"],
            "home_seed": ["1"],
            "home_nat_seed": ["14"],
            "away_team": [str(teams.indiana.pk)],
            "away_seed": ["3"],
            "live_stats": [
                "https://stats.statbroadcast.com/broadcast/?id=491945&vislive=ind"
            ],
            "first_pitch": ["2025-06-03-1800"],
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Indiana (3-seed)" in str(response.content)
    assert "at" in str(response.content)
    assert "no. 20" in str(response.content)
    assert "Kentucky (1-seed)" in str(response.content)
    assert "(#14 National Seed)" in str(response.content)


@pytest.mark.django_db
def test_add_game_post_asks_for_login_when_not_logged_in(client, teams):
    response = client.post(
        reverse("add_game"),
        {
            "home_team": [str(teams.indiana.pk)],
            "away_team": [str(teams.gm.pk)],
            "neutral_site": ["on"],
            "live_stats": [
                "https://stats.statbroadcast.com/broadcast/?id=491945&vislive=ind"
            ],
            "first_pitch": ["2025-02-14-1830"],
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Password:" in str(response.content)
