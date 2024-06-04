import pytest

from collections import namedtuple
from django.utils import timezone
from datetime import datetime, date

from player_tracking.models import Player, Transaction, AnnualRoster, MLBDraftDate
from live_game_blog.models import Team
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
        birthdate=date(2003, 7, 30),
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
    be2021 = Player.objects.create(
        first="Brooks",
        last="Ey",
        hsgrad_year=2021,
        bats="right",
        throws="right",
    )
    PlayerObj = namedtuple("PlayerOnj", "dt2022 br2022 aw2023 nm2021 be2021")
    return PlayerObj(
        dt2022=dt2022,
        br2022=br2022,
        aw2023=aw2023,
        nm2021=nm2021,
        be2021=be2021,
    )


@pytest.fixture
def transactions(client, players):
    current_tz = timezone.get_current_timezone()
    current_dt = datetime.now()
    dt_verbal = Transaction.objects.create(
        player=players.dt2022,
        trans_event="verbal", # need to aling with current choices
        trans_date=datetime(year=2021, month=3, day=11, hour=12, tzinfo=current_tz),
    )
    dt_nli = Transaction.objects.create(
        player=players.dt2022,
        trans_event="nli", # need to aling with current choices
        trans_date=datetime(year=2021, month=11, day=7, hour=12, tzinfo=current_tz),
    )
    be_portal = Transaction.objects.create(
        player=players.be2021,
        trans_event="Entered Transfer Portal",
        trans_date=date(current_dt.year, current_dt.month, current_dt.day)
    )
    TransObj = namedtuple("TransObj", "dt_verbal dt_nli be_portal")
    return TransObj(
        dt_verbal=dt_verbal,
        dt_nli=dt_nli,
        be_portal=be_portal,
    )


@pytest.fixture
def annual_rosters(client, players, teams):
    dt_2023 = AnnualRoster.objects.create(
        spring_year=2023,
        status="Spring Roster",
        player=players.dt2022,
        team=teams.indiana,
        jersey=5,
        primary_position="Corner Outfield",
        secondary_position="First Base",
    )
    dt_2024 = AnnualRoster.objects.create(
        spring_year=2024,
        status="Fall Roster",
        team=teams.indiana,
        player=players.dt2022,
        jersey=5,
        primary_position="Corner Outfield",
    )
    nm_2024 = AnnualRoster.objects.create(
        spring_year=2024,
        status="Fall Roster",
        player=players.nm2021,
        team=teams.indiana,
        jersey=20,
        primary_position="Centerfield",
    )
    nm_2023 = AnnualRoster.objects.create(
        spring_year=2023,
        status="Spring Roster",
        player=players.nm2021,
        team=teams.miami_oh,
        jersey=20,
        primary_position="Centerfield",
        secondary_position="Corner Outfield",
    )
    br_2023 = AnnualRoster.objects.create(
        spring_year=2023,
        status="Spring Roster",
        player=players.br2022,
        team=teams.indiana,
        jersey=51,
        primary_position="Pitcher",
    )
    AnnualRosterObj = namedtuple(
        "AnnualRosterObj",
        "dt_2023 dt_2024 nm_2023 nm_2024 br_2023"
    )
    return AnnualRosterObj(
        dt_2023=dt_2023,
        dt_2024=dt_2024,
        nm_2023=nm_2023,
        nm_2024=nm_2024,
        br_2023=br_2023,
    )


@pytest.fixture
def mlb_draft_date(client):
    birth_2024 = MLBDraftDate.objects.create(
        fall_year=2024,
        latest_birthdate=date(2003, 8, 1)
    )
    MLBDraftDateObj = namedtuple(
        "MLBDraftDateObj",
        "birth_2024"
    )
    return MLBDraftDateObj(
        birth_2024=birth_2024,
    )