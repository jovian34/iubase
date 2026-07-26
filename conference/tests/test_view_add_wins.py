import pytest

from django import urls

from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.conf_teams import conf_teams
from conference.tests.fixtures.conf_series_current import conf_series_current
from conference.tests.fixtures.form_data import forms
from live_game_blog.tests.fixtures.teams import teams

from conference import models as conf_models


@pytest.mark.django_db
def test_add_away_win_increases_win_by_one(admin_client, conferences, conf_teams, conf_series_current):
    response = admin_client.get(
        urls.reverse("add_away_win", args=[conf_series_current.iu_iowa.pk]),
        HTTP_HX_REQUEST="true",
    )
    series = conf_models.ConfSeries.objects.get(pk=conf_series_current.iu_iowa.pk)
    assert series.away_wins == 1.0
    assert series.home_wins == 0


@pytest.mark.django_db
def test_add_away_win_does_not_make_changes_without_perms(client, conferences, conf_teams, conf_series_current):
    response = client.get(
        urls.reverse("add_away_win", args=[conf_series_current.iu_iowa.pk]),
        HTTP_HX_REQUEST="true",
    )
    series = conf_models.ConfSeries.objects.get(pk=conf_series_current.iu_iowa.pk)
    assert series.away_wins == 0
    assert series.home_wins == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "view_name",
    (
        "add_away_win",
        "add_home_win",
        "add_tie",
    ),
)
def test_score_change_without_htmx_redirects_without_changing_score(
    admin_client,
    conferences,
    conf_teams,
    conf_series_current,
    view_name,
):
    original_series = conf_series_current.iu_iowa
    response = admin_client.get(
        urls.reverse(view_name, args=[original_series.pk]),
    )
    series = conf_models.ConfSeries.objects.get(pk=original_series.pk)

    expected_url = urls.reverse(
        "conf_schedule_week",
        kwargs={
            "spring_year": original_series.start_date.year,
            "month": original_series.start_date.month,
            "day": original_series.start_date.day,
        },
    )
    assert response.status_code == 302
    assert response.url == expected_url
    assert series.away_wins == 0
    assert series.home_wins == 0
    

@pytest.mark.django_db
def test_add_home_win_increases_win_by_one(admin_client, conferences, conf_teams, conf_series_current):
    response = admin_client.get(
        urls.reverse("add_home_win", args=[conf_series_current.iu_iowa.pk]),
        HTTP_HX_REQUEST="true",
    )
    series = conf_models.ConfSeries.objects.get(pk=conf_series_current.iu_iowa.pk)
    assert series.home_wins == 1.0
    assert series.away_wins == 0


@pytest.mark.django_db
def test_add_home_win_does_not_make_changes_without_perms(client, conferences, conf_teams, conf_series_current):
    response = client.get(
        urls.reverse("add_home_win", args=[conf_series_current.iu_iowa.pk]),
        HTTP_HX_REQUEST="true",)
    series = conf_models.ConfSeries.objects.get(pk=conf_series_current.iu_iowa.pk)
    assert series.home_wins == 0
    assert series.away_wins == 0


@pytest.mark.django_db
def test_add_tie_increases_wins_by_each_by_half(admin_client, conferences, conf_teams, conf_series_current):
    response = admin_client.get(
        urls.reverse("add_tie", args=[conf_series_current.iu_iowa.pk]),
        HTTP_HX_REQUEST="true",
    )
    series = conf_models.ConfSeries.objects.get(pk=conf_series_current.iu_iowa.pk)
    assert series.home_wins == 0.5
    assert series.away_wins == 0.5
