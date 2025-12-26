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
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from live_game_blog.tests.fixtures.blog import entries
from live_game_blog.tests.fixtures.form_data import forms
from live_game_blog.tests.fixtures.scoreboards import scoreboards
from conference.tests.fixtures.conferences import conferences


@pytest.mark.django_db
def test_add_blog_entry_plus_scoreboard_form_no_perms_shows_forbidden(
    client, logged_user_schwarbs, games, forms, scoreboards
):
    response = client.post(
        reverse("add_blog_plus_scoreboard", args=[games.iu_duke.pk]),
        forms.iu_holds_duke,
        follow=True,
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_blog_entry_plus_scoreboard_form(
    client, superuser_houston, games, forms, scoreboards
):
    response = client.post(
        reverse("add_blog_plus_scoreboard", args=[games.iu_duke.pk]),
        forms.iu_holds_duke,
        follow=True,
    )
    assert response.status_code == 200
    assert "Indiana holds Duke to one run" in str(response.content)
    assert "Jeremy" in str(response.content)
    assert "End of bottom of inning 2" in str(response.content)


@pytest.mark.django_db
def test_add_blog_entry_plus_scoreboard_markdown_to_html(
    admin_client, games, forms, scoreboards
):
    response = admin_client.post(
        reverse("add_blog_plus_scoreboard", args=[games.iu_duke.pk]),
        forms.iu_slams_duke,
        follow=True,
    )
    assert response.status_code == 200
    assert "<h2>DEVIN TAYLOR SALAMI!!!!</h2>" in str(response.content)
    assert "Top of inning 4 with 1 outs" in str(response.content)


@pytest.mark.django_db
def test_add_blog_entry_plus_scoreboard_form_shows_forbidden_not_logged_in(
    client, games, forms
):
    response = client.post(
        reverse("add_blog_plus_scoreboard", args=[games.iu_duke.pk]),
        forms.iu_holds_duke,
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_add_blog_plus_scoreboard_end_of_bottom_fills_form_with_top_of_inning(
    admin_client, games, scoreboards
):
    response = admin_client.get(
        reverse("add_blog_plus_scoreboard", args=[games.iu_mo_rain.pk]),
    )
    assert response.status_code == 200
    assert 'value="Top" selected' in str(response.content)


@pytest.mark.django_db
def test_get_add_blog_plus_scoreboard_end_of_top_fills_form_with_bottom_of_inning(
    admin_client, games, scoreboards
):
    response = admin_client.get(
        reverse("add_blog_plus_scoreboard", args=[games.iu_uk_sat.pk]),
    )
    assert response.status_code == 200
    assert 'value="Bottom" selected' in str(response.content)


@pytest.mark.django_db
def test_get_add_blog_plus_scoreboard_ip_fills_form_with_top_of_inning(
    admin_client, games, scoreboards
):
    response = admin_client.get(
        reverse("add_blog_plus_scoreboard", args=[games.iu_coastal_ip.pk]),
    )
    assert response.status_code == 200
    assert 'value="Top" selected' in str(response.content)


@pytest.mark.django_db
def test_get_add_blog_plus_scoreboard_shows_team_names_in_form_labels(
    admin_client, games, scoreboards
):
    response = admin_client.get(
        reverse("add_blog_plus_scoreboard", args=[games.iu_coastal_ip.pk]),
    )
    assert response.status_code == 200
    assert "Coastal Carolina Runs Scored" in str(response.content)
    assert "Coastal Carolina Hits" in str(response.content)
    assert "Indiana Errors" in str(response.content)
