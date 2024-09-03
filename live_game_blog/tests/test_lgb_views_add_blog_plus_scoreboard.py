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
from live_game_blog.tests.fixtures.form_data import forms
from live_game_blog.tests.fixtures.scoreboards import scoreboards


@pytest.mark.django_db
def test_add_blog_entry_plus_scoreboard_form(client, logged_user_schwarbs, games, forms):
    response = client.post(
        reverse("add_blog_plus_scoreboard", args=[games.iu_duke.pk]),
        forms.iu_holds_duke,
        follow=True,
    )
    assert response.status_code == 200
    assert "Indiana holds Duke to one run" in str(response.content)
    assert "Kyle" in str(response.content)
    assert "End of bottom of inning 2" in str(response.content)


@pytest.mark.django_db
def test_add_blog_entry_plus_scoreboard_makrkdown_to_html(client, logged_user_schwarbs, games, forms):
    response = client.post(
        reverse("add_blog_plus_scoreboard", args=[games.iu_duke.pk]),
        forms.iu_slams_duke,
        follow=True,
    )
    assert response.status_code == 200
    assert "<h2>DEVIN TAYLOR SALAMI!!!!</h2>" in str(response.content)
    assert "Top of inning 4 with 1 outs" in str(response.content)


@pytest.mark.django_db
def test_add_blog_entry_plus_scoreboard_form_redirects_not_logged_in(client, user_not_logged_in, games, forms):
    response = client.post(
        reverse("add_blog_plus_scoreboard", args=[games.iu_duke.pk]),
        forms.iu_holds_duke,
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_blog_entry_plus_scoreboard_form_redirects_not_logged_in(client, user_not_logged_in, games, forms):
    response = client.post(
        reverse("add_blog_plus_scoreboard", args=[games.iu_duke.pk]),
        forms.iu_holds_duke,
        follow=True,
    )
    assert response.status_code == 200
    assert "Password:" in str(response.content)