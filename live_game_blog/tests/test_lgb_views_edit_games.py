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
from live_game_blog.tests.fixtures.form_data import forms
from live_game_blog.tests.fixtures.scoreboards import scoreboards
from conference.tests.fixtures.conferences import conferences
from django_project.tests import clean_text

from live_game_blog.views import live_game_blog
from live_game_blog import models as lgb_models


this_year = datetime.today().year


@pytest.mark.django_db
def test_edit_lgb_game_renders_change_form(admin_client, games, scoreboards, entries):
    response = admin_client.get(reverse("edit_game_info", args=[games.iu_coastal_ip.pk]))
    assert response.status_code == 200
    output = clean_text.get_and_clean_content_from_response(response)
    assert "20" in output


@pytest.mark.django_db
def test_edit_lgb_game_changes_event_name(admin_client, games, scoreboards, entries, forms):
    response = admin_client.post(
        reverse("edit_game_info", args=[games.iu_coastal_ip.pk]),
        forms.edit_iu_coastal_ip,
        follow=True,
    )
    assert response.status_code == 200
    assert "Baseball at the Beach" in response.content.decode()