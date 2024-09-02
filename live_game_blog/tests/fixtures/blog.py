import pytest

from collections import namedtuple
from datetime import timedelta

from live_game_blog.models import BlogEntry
from live_game_blog.tests.fixtures.games import games
from live_game_blog.tests.fixtures.scoreboards import scoreboards
from accounts.tests.fixtures import (
    user_not_logged_in,
    user_iubase17,
    logged_user_schwarbs,
)


@pytest.fixture
def entries(client, games, user_not_logged_in, scoreboards):
    blog_uk_mon_y = BlogEntry.objects.create(
        game=games.iu_uk_mon,
        author=user_not_logged_in,
        blog_time=games.iu_uk_mon.first_pitch + timedelta(minutes=10),
        blog_entry="Bothwell walks the first batter",
        include_scoreboard=False,
    )
    blog_uk_mon_z = BlogEntry.objects.create(
        game=games.iu_uk_mon,
        author=user_not_logged_in,
        blog_time=games.iu_uk_mon.first_pitch + timedelta(minutes=165),
        blog_entry="Kentucky moves on to Super Regionals",
        include_scoreboard=True,
        scoreboard=scoreboards.score_uk_mon,
    )
    BlogEntryObj = namedtuple(
        "BlogEntryObj",
        "blog_uk_mon_y blog_uk_mon_z",
    )
    return BlogEntryObj(
        blog_uk_mon_y=blog_uk_mon_y,
        blog_uk_mon_z=blog_uk_mon_z,
    )