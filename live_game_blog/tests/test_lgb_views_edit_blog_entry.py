import pytest

# from datetime import datetime, timedelta
from django.urls import reverse

from live_game_blog.tests.fixtures.games import (
    games,
    logged_user_schwarbs,
    user_not_logged_in,
    user_iubase17,
)
from live_game_blog.tests.fixtures.teams import teams
from live_game_blog.tests.fixtures.blog import entries
from live_game_blog.tests.fixtures.scoreboards import scoreboards


@pytest.mark.django_db
def test_edit_blog_entry_adds_text(client, logged_user_schwarbs, games, entries):
    response = client.post(
        reverse("edit_blog_entry", args=[entries.blog_uk_mon_y.pk]),
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
    client, logged_user_schwarbs, games, entries
):
    response = client.post(
        reverse("edit_blog_entry", args=[entries.blog_uk_mon_z.pk]),
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