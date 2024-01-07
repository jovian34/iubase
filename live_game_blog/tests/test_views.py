import pytest

from datetime import datetime, timedelta
from django.urls import reverse

from live_game_blog.tests.fixtures import teams, games, scoreboard, logged_user_schwarbs, blog_entries, user_not_logged_in, user_iubase17

@pytest.mark.django_db
def test_games_list_page_renders_road_and_neutral_future(client, teams, games):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "Indiana" in str(response.content)
    assert "versus" in str(response.content)
    assert "at" in str(response.content)

@pytest.mark.django_db
def test_games_list_page_does_not_render_past_games(client, teams, games, scoreboard):
    response = client.get(reverse("games"))
    assert response.status_code == 200
    assert "Coastal Carolina" in str(response.content)
    assert "Kentucky" not in str(response.content)

@pytest.mark.django_db
def test_games_list_page_does_not_render_four_games_out(client, teams, games, scoreboard):
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
    assert "Indiana at Kentucky" in str(response.content)
    assert "(FINAL)" in str(response.content)
    assert "Kentucky moves on to Super Regionals" in str(response.content)

@pytest.mark.django_db
def test_edit_live_single_game_blog_page_renders(client, games, scoreboard, blog_entries, logged_user_schwarbs):
    response = client.get(reverse("edit_live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_edit_live_single_game_blog_page_redirects_not_logged_in(client, games, scoreboard, blog_entries):
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
        follow=True                       
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
        follow=True                       
    )
    assert response.status_code == 200
    assert "Adding to the Duke Blog" in str(response.content)
    assert "Kyle" in str(response.content)

@pytest.mark.django_db
def test_add_blog_entry_only_x_embed_post_form(client, logged_user_schwarbs, user_iubase17, games, scoreboard):
    response = client.post(
        reverse("add_blog_entry_only", args=[games.iu_duke.pk]),
        { 
            "blog_entry": "<li>Adding to the Duke Blog",
            "is_raw_html": True,
            "is_x_embed": True,
        },
        follow=True                       
    )
    assert response.status_code == 200
    assert "<li>Adding to the Duke Blog" in str(response.content)
    assert "entry by @iubase17" in str(response.content)


@pytest.mark.django_db
def test_add_team_and_confirm_team_is_selectable_for_add_game(client, logged_user_schwarbs):
    response = client.post(
        reverse("add_team"),
        {
            "team_name": "Purdue Ft. Wayne",
            "mascot": "Mastodons",
            "logo": "https://cdn.d1baseball.com/uploads/2023/12/21143914/iupufw.png",
            "stats": "https://d1baseball.com/team/iupufw/stats/",
            "roster": "https://gomastodons.com/sports/baseball/roster",
        }
    )
    assert response.status_code == 302
    response = client.get(reverse("add_game"))
    assert "Purdue Ft. Wayne" in str(response.content)


@pytest.mark.django_db
def test_add_team_post_asks_for_login_when_not_logged_in(client):
    response = client.post(
        reverse("add_team"),
        {
            "team_name": "Purdue Ft. Wayne",
            "mascot": "Mastodons",
            "logo": "https://cdn.d1baseball.com/uploads/2023/12/21143914/iupufw.png",
            "stats": "https://d1baseball.com/team/iupufw/stats/",
            "roster": "https://gomastodons.com/sports/baseball/roster",
        },
        follow=True
    )
    assert response.status_code == 200
    assert "Password:" in str(response.content)


@pytest.mark.django_db
def test_add_game(client, logged_user_schwarbs, teams, games, scoreboard):
    response = client.post(
        reverse("add_game"),
        {
            'home_team': [str(teams.indiana.pk)],
            'away_team': [str(teams.gm.pk)],
            'neutral_site': ['on'],
            'live_stats': ['https://stats.statbroadcast.com/broadcast/?id=491945&vislive=ind'],
            'first_pitch': ['2025-02-14-1830']
        },
        follow=True
    )
    assert response.status_code == 200
    assert "George Mason vs. Indiana" in str(response.content)
    assert "Feb. 14, 2025, 6:30 p.m. first pitch" in str(response.content)


@pytest.mark.django_db
def test_add_game_post_asks_for_login_when_not_logged_in(client, teams):
    response = client.post(
        reverse("add_game"),
        {
            'home_team': [str(teams.indiana.pk)],
            'away_team': [str(teams.gm.pk)],
            'neutral_site': ['on'],
            'live_stats': ['https://stats.statbroadcast.com/broadcast/?id=491945&vislive=ind'],
            'first_pitch': ['2025-02-14-1830']
        },
        follow=True
    )
    assert response.status_code == 200
    assert "Password:" in str(response.content)
