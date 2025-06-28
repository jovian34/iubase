import pytest

from django.urls import reverse

from live_game_blog.tests.fixtures.games import (
    games,
    logged_user_schwarbs,
    user_not_logged_in,
    user_iubase17,
    superuser_houston,
)
from live_game_blog.tests.fixtures.teams import teams
from live_game_blog.tests.fixtures.blog import entries
from live_game_blog.tests.fixtures.scoreboards import scoreboards


@pytest.mark.django_db
def test_add_blog_entry_only_get_renders(
    client, superuser_houston, games, scoreboards
):
    response = client.get(reverse("add_blog_entry_only", args=[games.iu_duke.pk]))
    assert response.status_code == 200
    assert "Content of Blog" in str(response.content)


@pytest.mark.django_db
def test_add_blog_entry_only_get_no_perms_shows_forbidden(
    client, logged_user_schwarbs, games, scoreboards
):
    response = client.get(reverse("add_blog_entry_only", args=[games.iu_duke.pk]))
    assert response.status_code == 200
    assert "Forbidden Error Recorded" in str(response.content)


@pytest.mark.django_db
def test_add_blog_entry_only_post_form(
    client, superuser_houston, games, scoreboards
):
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
    assert "Jeremy" in str(response.content)


@pytest.mark.django_db
def test_add_blog_entry_only_photo_post_form_shows_forbidden(
    client, logged_user_schwarbs, games, scoreboards
):
    response = client.post(
        reverse("add_blog_entry_only", args=[games.iu_duke.pk]),
        {
            "blog_entry": "https://live.staticflickr.com/65535/54013610622_61d5c92ebc_o.jpg",
            "is_x_embed": False,
            "is_photo_only": True,
        },
    )
    assert response.status_code == 200
    assert "Forbidden Error Recorded" in str(response.content)


@pytest.mark.django_db
def test_add_blog_entry_only_photo_post_form_no_perms_shows_forbidden(
    client, logged_user_schwarbs, games, scoreboards
):
    response = client.post(
        reverse("add_blog_entry_only", args=[games.iu_duke.pk]),
        {
            "blog_entry": "https://live.staticflickr.com/65535/54013610622_61d5c92ebc_o.jpg",
            "is_x_embed": False,
            "is_photo_only": True,
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Forbidden Error Recorded" in str(response.content)


@pytest.mark.django_db
def test_add_blog_entry_only_photo_post_form(
    client, superuser_houston, games, scoreboards
):
    response = client.post(
        reverse("add_blog_entry_only", args=[games.iu_duke.pk]),
        {
            "blog_entry": "https://live.staticflickr.com/65535/54013610622_61d5c92ebc_o.jpg",
            "is_x_embed": False,
            "is_photo_only": True,
        },
        follow=True,
    )
    assert response.status_code == 200
    assert 'class="lgb-featured-image">' in str(response.content)


@pytest.mark.django_db
def test_add_blog_entry_only_post_not_logged_in_shows_forbidden(
    client, user_not_logged_in, games, scoreboards
):
    response = client.post(
        reverse("add_blog_entry_only", args=[games.iu_duke.pk]),
        {
            "blog_entry": "Adding to the Duke Blog",
            "is_x_embed": False,
        },
    )
    assert response.status_code == 200
    assert "Forbidden Error Recorded" in str(response.content)


@pytest.mark.django_db
def test_add_blog_entry_only_post_not_logged_in_shows_forbidden(
    client, user_not_logged_in, games, scoreboards
):
    response = client.post(
        reverse("add_blog_entry_only", args=[games.iu_duke.pk]),
        {
            "blog_entry": "Adding to the Duke Blog",
            "is_x_embed": False,
        },
    )
    assert response.status_code == 200
    assert "Forbidden Error Recorded" in str(response.content)


@pytest.mark.django_db
def test_add_blog_entry_only_x_embed_post_no_perms_shows_forbidden(
    client, logged_user_schwarbs, user_iubase17, games, scoreboards
):
    response = client.post(
        reverse("add_blog_entry_only", args=[games.iu_duke.pk]),
        {
            "blog_entry": "<li>Adding to the Duke Blog",
            "is_raw_html": True,
            "is_x_embed": True,
        },
    )
    assert response.status_code == 200
    assert "Forbidden Error Recorded" in str(response.content)


@pytest.mark.django_db
def test_add_blog_entry_only_x_embed_post_form(
    client, superuser_houston, user_iubase17, games, scoreboards
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
def test_add_blog_entry_only_markdown_converts_to_html(
    client, superuser_houston, games, scoreboards
):
    response = client.post(
        reverse("add_blog_entry_only", args=[games.iu_duke.pk]),
        {
            "blog_entry": "# Adding to the Duke Blog",
            "is_raw_html": False,
            "is_x_embed": False,
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "<h1>Adding to the Duke Blog</h1>" in str(response.content)
