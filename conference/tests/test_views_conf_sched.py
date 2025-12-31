import pytest
import datetime
from django import urls

from live_game_blog.tests.fixtures.teams import teams
from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.conf_teams import conf_teams
from conference.tests.fixtures.conf_series import conf_series

from conference import year
from conference import models as conf_models



@pytest.mark.django_db
def test_current_year_b1g_schedule_renders(client, teams, conferences, conf_teams, conf_series):
    series = conf_models.ConfSeries.objects.all().order_by("start_date")[0]
    response = client.get(urls.reverse("conf_schedule", args=[year.get_spring_year()]))
    assert response.status_code == 200
    assert "2026 B1G Schedule" in response.content.decode()
    assert f"Week 1 starting {series.start_date:%A}, March 7:" in response.content.decode()
    assert "https://web2.ncaa.org/ncaa_style/img/All_Logos/sm/110.gif" in response.content.decode()


@pytest.mark.django_db
def test_current_year_b1g_schedule_renders_in_correct_order(client, teams, conferences, conf_teams, conf_series):
    response = client.get(urls.reverse("conf_schedule", args=[year.get_spring_year()]))
    assert response.status_code == 200
    output = response.content.decode()
    w1 = output.find("Week 1")
    w2 = output.find("Week 2")
    assert w1 < w2
