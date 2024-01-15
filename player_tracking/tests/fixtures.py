import pytest

from collections import namedtuple
from django.utils import timezone
from datetime import datetime

from player_tracking.models import Player, Transaction, AnnualRoster
from live_game_blog.tests.fixtures import teams


@pytest.fixture
def players(client):
    dt2022 = Player.objects.create(
        first="Devin", last="Taylor", hsgrad_year=2022, bats="left", throws="left"
    )
    br2022 = Player.objects.create(
        first="Brayden",
        last="Risedorph",
        hsgrad_year=2022,
        bats="right",
        throws="right",
    )
    aw2023 = Player.objects.create(
        first="Andrew", last="Wiggings", hsgrad_year=2023, bats="left", throws="right"
    )
    nm2021 = Player.objects.create(
        first="Nick",
        last="Mitchell",
        hsgrad_year=2021,
        bats="left",
        throws="right",
    )
    PlayerObj = namedtuple("PlayerOnj", "dt2022 br2022 aw2023 nm2021")
    return PlayerObj(
        dt2022=dt2022,
        br2022=br2022,
        aw2023=aw2023,
        nm2021=nm2021,
    )


@pytest.fixture
def transactions(client, players):
    current_tz = timezone.get_current_timezone()
    dt_verbal = Transaction.objects.create(
        player=players.dt2022,
        trans_event="verbal",
        trans_date=datetime(year=2021, month=3, day=11, hour=12, tzinfo=current_tz),
    )
    dt_nli = Transaction.objects.create(
        player=players.dt2022,
        trans_event="nli",
        trans_date=datetime(year=2021, month=11, day=7, hour=12, tzinfo=current_tz),
    )
    TransObj = namedtuple("TransObj", "dt_verbal dt_nli")
    return TransObj(
        dt_verbal=dt_verbal,
        dt_nli=dt_nli,
    )


@pytest.fixture
def annual_roster(client, players, teams):
    dt_2023 = AnnualRoster.objects.create(
        spring_year=2023,
        player=players.dt2022,
        team=teams.indiana,
        jersey=5,
        primary_position="OF",
        secondary_position="1B",
    )
    dt_2024 = AnnualRoster.objects.create(
        spring_year=2024,
        player=players.dt2022,
        jersey=5,
        primary_position="OF",
    )
    AnnualRosterObj = namedtuple("AnnualRosterObj", "dt_2023 dt_2024")
    return AnnualRosterObj(
        dt_2023=dt_2023,
        dt_2024=dt_2024,
    )
