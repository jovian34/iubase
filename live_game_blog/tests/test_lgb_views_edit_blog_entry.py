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
def test_edit_blog_entry_get_renders_with_scoreboard(client, logged_user_schwarbs, games, entries, scoreboards):
    response = client.get(reverse("edit_blog_entry", args=[entries.blog_uk_mon_y.pk]))
    assert response.status_code == 200
    assert "Content of Blog" in str(response.content)
    assert "Bothwell walks the first batter" in str(response.content)    


@pytest.mark.django_db
def test_edit_blog_entry_get_renders_without_scoreboard(client, logged_user_schwarbs, games, entries, scoreboards):
    response = client.get(reverse("edit_blog_entry", args=[entries.blog_uk_mon_z.pk]))
    assert response.status_code == 200
    assert "Content of Blog" in str(response.content)
    assert "Kentucky moves on to Super Regionals" in str(response.content)                        


@pytest.mark.django_db
def test_edit_blog_entry_adds_text(client, logged_user_schwarbs, games, entries, scoreboards):
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
    client, logged_user_schwarbs, games, entries, forms, scoreboards
):
    response = client.post(
        reverse("edit_blog_entry", args=[entries.blog_uk_mon_z.pk]),
        forms.edit_blog_uk_wins,
        follow=True,
    )
    assert response.status_code == 200
    assert "8 hits" not in str(response.content)
    assert "2 errors" in str(response.content)


@pytest.mark.django_db
def test_edit_blog_entry_redirects_when_not_logged_in(
    client, games, entries, forms, scoreboards
):
    response = client.post(
        reverse("edit_blog_entry", args=[entries.blog_uk_mon_z.pk]),
        forms.edit_blog_uk_wins,
        follow=False,
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_blog_entry_asks_for_password_when_not_logged_in_post(
    client, games, entries, forms, scoreboards
):
    response = client.post(
        reverse("edit_blog_entry", args=[entries.blog_uk_mon_z.pk]),
        forms.edit_blog_uk_wins,
        follow=True,
    )
    assert response.status_code == 200
    assert "Password:" in str(response.content)


@pytest.mark.django_db
def test_edit_blog_entry_asks_for_password_when_not_logged_in_get(
    client, games, entries, forms, scoreboards
):
    response = client.get(
        reverse("edit_blog_entry", args=[entries.blog_uk_mon_z.pk]),
        follow=True,
    )
    assert response.status_code == 200
    assert "Password:" in str(response.content)