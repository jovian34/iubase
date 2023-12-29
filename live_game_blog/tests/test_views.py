import pytest
from django.urls import reverse

from live_game_blog.tests.fixtures import teams, games, scoreboard, logged_user_schwarbs, blog_entries, user_not_logged_in

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
def test_add_blog_entry_only_post_form(client, logged_user_schwarbs, blog_entries, games):
    response = client.post(
        reverse("add_blog_entry_only", args=[games.iu_duke.pk]),
        { "blog_entry": "Adding to the Duke Blog" },
        follow=True                       
    )
    assert response.status_code == 200
    assert "Adding to the Duke Blog" in str(response.content)

@pytest.mark.django_db
def test_add_blog_entry_plus_scoreboard_form(client, logged_user_schwarbs, blog_entries, games):
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