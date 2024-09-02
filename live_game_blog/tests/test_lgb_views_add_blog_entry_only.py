import pytest

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
def test_add_blog_entry_only_post_form(client, logged_user_schwarbs, games, scoreboards):
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
    client, logged_user_schwarbs, user_iubase17, games, scoreboards
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