import pytest
from datetime import datetime

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


this_year = datetime.today().year


@pytest.mark.django_db
def test_live_single_game_blog_page_renders(client, games, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    assert "Joey" in str(response.content)
    assert "Indiana at Kentucky," in str(response.content)
    assert "(FINAL)" in str(response.content)
    assert "Kentucky moves on to Super Regionals" in str(response.content)
    assert "stats" in str(response.content)
    assert "roster" in str(response.content)


@pytest.mark.django_db
def test_live_single_in_progress_game_blog_page_renders_in_reverse_order(client, games, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_coastal_ip.pk]))
    assert response.status_code == 200
    output = str(response.content)
    late = output.find("Pete Haas warming as the seventh starts")
    early = output.find("Gavin Seebold back out for the third inning")
    assert late < early


@pytest.mark.django_db
def test_live_single_complete_game_blog_page_renders_in_chron_order(client, games, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    output = str(response.content)
    late = output.find("Kentucky moves on to Super Regionals")
    early = output.find("Bothwell walks the first batter")
    assert late > early


@pytest.mark.django_db
def test_live_single_complete_game_blog_page_renders_photo_html(client, games, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    assert 'class="lgb-featured-image">' in str(response.content)


@pytest.mark.django_db
def test_non_existent_game_raises_404_error(
    client, games, scoreboards, entries
):
    response = client.get(reverse("live_game_blog", args=[58479574]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_roster_url_renders_with_year_specified_and_adds_slash_before_year(client, games, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_duke.pk]))
    assert response.status_code == 200
    assert f"https://iuhoosiers.com/sports/baseball/roster/{this_year}/" in str(response.content)


@pytest.mark.django_db
def test_roster_url_renders_with_year_specified_and_keeps_slash_before_year(client, games, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_duke.pk]))
    assert response.status_code == 200
    assert f"https://goduke.com/sports/baseball/roster/{this_year}/" in str(response.content)


@pytest.mark.django_db
def test_roster_url_renders_with_last_year_specified_and_keeps_slash_before_year(client, games, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_duke_ly.pk]))
    assert response.status_code == 200
    assert f"https://goduke.com/sports/baseball/roster/{this_year - 1}/" in str(response.content)


@pytest.mark.django_db
def test_roster_url_fall_game_renders_with_next_spring_roster(client, games, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_duke_23_fall.pk]))
    assert response.status_code == 200
    assert f"https://goduke.com/sports/baseball/roster/2024/" in str(response.content)


@pytest.mark.django_db
def test_lgb_shows_weekday(client, games, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_duke_23_fall.pk]))
    assert response.status_code == 200
    assert "Wed, Oct. 4, 2023," in str(response.content)
