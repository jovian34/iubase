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
from live_game_blog.tests.fixtures.stadiums import stadiums
from live_game_blog.tests.fixtures.stadium_configs import stadium_configs
from live_game_blog.tests.fixtures.blog import entries
from live_game_blog.tests.fixtures.scoreboards import scoreboards
from conference.tests.fixtures.conf_teams import conf_teams
from conference.tests.fixtures.conferences import conferences
from django_project.tests import clean_text

from live_game_blog.views import live_game_blog
from live_game_blog import models as lgb_models


this_year = datetime.today().year


@pytest.mark.django_db
def test_live_single_game_blog_page_renders(client, games, scoreboards, entries, conf_teams, conferences):
    response = client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    assert "Joey" in response.content.decode()
    assert "Indiana at Kentucky," in response.content.decode()
    assert "(FINAL)" in response.content.decode()
    assert "Kentucky moves on to Super Regionals" in response.content.decode()
    assert "stats" in response.content.decode()
    assert "roster" in response.content.decode()
    assert "https://cdn.d1baseball.com/uploads/2023/12/21135542/southeastern-conference.png" in response.content.decode()


@pytest.mark.django_db
def test_live_single_completed_game_blog_page_does_not_show_live_stats_link(client, games, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    assert "https://t.co/Odg1uF46xM" not in response.content.decode()


@pytest.mark.django_db
def test_live_single_in_progress_game_blog_page_renders_in_reverse_order(
    client, games, scoreboards, entries
):
    response = client.get(reverse("live_game_blog", args=[games.iu_coastal_ip.pk]))
    assert response.status_code == 200
    output = response.content.decode()
    late = output.find("Pete Haas warming as the seventh starts")
    early = output.find("Gavin Seebold back out for the third inning")
    assert early != -1  # verifies early was found
    assert late < early


@pytest.mark.django_db
def test_live_single_in_progress_game_blog_page_renders_live_stats_link(
    client, games, scoreboards, entries
):
    response = client.get(reverse("live_game_blog", args=[games.iu_coastal_ip.pk]))
    assert response.status_code == 200
    assert "http://stats.statbroadcast.com/broadcast/?id=499358" in response.content.decode()


@pytest.mark.django_db
def test_live_single_future_game_blog_page_renders_first_pitch_in_title(
    client, games, scoreboards, entries
):
    response = client.get(reverse("live_game_blog", args=[games.iu_gm_fall.pk]))
    assert response.status_code == 200
    output = clean_text.get_and_clean_content_from_response(response)
    late = output.find("</title>")
    early = output.find(".m. first pitch")
    assert early != -1  # verifies early was found
    assert late > early


@pytest.mark.django_db
def test_live_single_in_progress_game_blog_page_renders_score_and_inning_in_title(
    client, games, scoreboards, entries
):
    response = client.get(reverse("live_game_blog", args=[games.iu_coastal_ip.pk]))
    assert response.status_code == 200
    output = clean_text.get_and_clean_content_from_response(response)
    late = output.find("</title>")
    early = output.find("Indiana at Coastal Carolina, 0-6 Top 3")
    assert early != -1  # verifies early was found
    assert late > early
    assert "FINAL" not in output


@pytest.mark.django_db
def test_live_single_complete_game_blog_page_renders_score_in_title(
    client, games, scoreboards, entries
):
    response = client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    output = clean_text.get_and_clean_content_from_response(response)
    late = output.find("</title>")
    early = output.find("Indiana at Kentucky, 2-4 Top 9 (FINAL)")
    assert early != -1  # verifies early was found
    assert late > early


@pytest.mark.django_db
def test_live_single_complete_game_blog_page_renders_in_chron_order(
    client, games, scoreboards, entries
):
    response = client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    output = response.content.decode()
    late = output.find("Kentucky moves on to Super Regionals")
    early = output.find("Bothwell walks the first batter")
    assert early != -1  # verifies early was found
    assert late > early


@pytest.mark.django_db
def test_live_single_complete_game_blog_page_renders_final_scoreboard_at_top(
    client, games, scoreboards, entries
):
    response = client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    output = response.content.decode()
    early = output.find("<p><b>Hoosiers</b>: <b>2</b> runs |")
    late = output.find("Bothwell walks the first batter")
    assert early != -1  # verifies early was found
    assert late > early


@pytest.mark.django_db
def test_live_single_complete_game_blog_page_renders_photo_html(
    client, games, scoreboards, entries
):
    response = client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    assert 'class="lgb-featured-image">' in response.content.decode()


@pytest.mark.django_db
def test_non_existent_game_raises_404_error(client, games, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[58479574]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_roster_url_renders_with_year_specified_and_adds_slash_before_year(
    client, games, scoreboards, entries
):
    response = client.get(reverse("live_game_blog", args=[games.iu_duke.pk]))
    spring_year = live_game_blog.set_spring_year(games.iu_duke)
    assert response.status_code == 200
    assert f"https://iuhoosiers.com/sports/baseball/roster/{spring_year}/" in str(
        response.content
    )


@pytest.mark.django_db
def test_roster_url_renders_special_case_roster_academic_year(
    client, games, scoreboards, entries
):
    response = client.get(reverse("live_game_blog", args=[games.iu_iowa.pk]))
    assert response.status_code == 200
    iowa_roster_url = f"https://hawkeyesports.com/sports/baseball/roster/season/{this_year + 2}-{this_year - 1997}"
    assert iowa_roster_url in response.content.decode()


@pytest.mark.django_db
def test_roster_url_renders_with_year_specified_and_keeps_slash_before_year(
    client, games, scoreboards, entries
):
    response = client.get(reverse("live_game_blog", args=[games.iu_duke.pk]))
    spring_year = live_game_blog.set_spring_year(games.iu_duke)
    assert response.status_code == 200
    assert f"https://goduke.com/sports/baseball/roster/{spring_year}/" in str(
        response.content
    )


@pytest.mark.django_db
def test_roster_url_renders_with_last_year_specified_and_keeps_slash_before_year(
    client, games, scoreboards, entries
):
    response = client.get(reverse("live_game_blog", args=[games.iu_duke_ly.pk]))
    spring_year = live_game_blog.set_spring_year(games.iu_duke_ly)
    assert response.status_code == 200
    assert f"https://goduke.com/sports/baseball/roster/{spring_year}/" in str(
        response.content
    )


@pytest.mark.django_db
def test_roster_url_fall_game_renders_with_next_spring_roster(
    client, games, scoreboards, entries
):
    response = client.get(reverse("live_game_blog", args=[games.iu_duke_23_fall.pk]))
    assert response.status_code == 200
    assert f"https://goduke.com/sports/baseball/roster/2024/" in response.content.decode()


@pytest.mark.django_db
def test_lgb_shows_weekday(client, games, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_duke_23_fall.pk]))
    assert response.status_code == 200
    assert "Wed, Oct. 4, 2023," in response.content.decode()


@pytest.mark.django_db
def test_lgb_shows_adds_and_edits_with_perms(admin_client, games, scoreboards, entries):
    response = admin_client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    assert "Add Blog Entry Only" in response.content.decode()
    assert "Add Blog Entry plus Scoreboard" in response.content.decode()
    assert "Edit Entry" in response.content.decode()
    assert "Edit Game Info" in response.content.decode()


@pytest.mark.django_db
def test_lgb_shows_no_adds_or_edits_without_perms(client, games, logged_user_schwarbs, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    assert "Add Blog Entry Only" not in response.content.decode()
    assert "Add Blog Entry plus Scoreboard" not in response.content.decode()
    assert "Edit Entry" not in response.content.decode()
    assert "Edit Game Info" not in response.content.decode()


@pytest.mark.django_db
def test_lgb_shows_no_adds_or_edits_not_logged_in(client, games, scoreboards, entries):
    response = client.get(reverse("live_game_blog", args=[games.iu_uk_mon.pk]))
    assert response.status_code == 200
    assert "Add Blog Entry Only" not in response.content.decode()
    assert "Add Blog Entry plus Scoreboard" not in response.content.decode()
    assert "Edit Entry" not in response.content.decode()


@pytest.mark.django_db
def test_set_spring_year_sets_october_to_next_spring(games):
    assert live_game_blog.set_spring_year(games.iu_duke_23_fall) == 2024


@pytest.mark.django_db
def test_set_spring_year_sets_february_to_same_spring(games):
    assert live_game_blog.set_spring_year(games.iu_duke_69_spring) == 2069