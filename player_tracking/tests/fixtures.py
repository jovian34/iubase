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
        first="Andrew", 
        last="Wiggings", 
        hsgrad_year=2023, 
        bats="left", 
        throws="right"
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
    jm2019 = Player.objects.create(
        first="Jack",
        last="Moffitt",
        hsgrad_year=2019,
        bats="right",
        throws="right",
    )
    gh2024 = Player.objects.create(
        first="Grant",
        last="Hollister",
        hsgrad_year=2024,
        bats="left",
        throws="right",
    )
    PlayerObj = namedtuple(
        "PlayerOnj", 
        "dt2022 br2022 aw2023 nm2021 be2021 jm2019 gh2024"
    )
    return PlayerObj(
        dt2022=dt2022,
        br2022=br2022,
        aw2023=aw2023,
        nm2021=nm2021,
        be2021=be2021,
        jm2019=jm2019,
        gh2024=gh2024,
    )


@pytest.fixture
def players_last_year_set(client):
    dt2022 = Player.objects.create(
        first="Devin",
        last="Taylor",
        hsgrad_year=2022,
        last_spring=2026,
        bats="left",
        throws="left"
    )
    br2022 = Player.objects.create(
        first="Brayden",
        last="Risedorph",
        hsgrad_year=2022,
        last_spring=2026,
        birthdate=date(2003, 7, 30),
        bats="right",
        throws="right",
    )
    aw2023 = Player.objects.create(
        first="Andrew", 
        last="Wiggings", 
        hsgrad_year=2023,
        last_spring=2027, 
        bats="left", 
        throws="right"
    )
    nm2021 = Player.objects.create(
        first="Nick",
        last="Mitchell",
        hsgrad_year=2021,
        last_spring=2025,
        bats="left",
        throws="right",
    )
    be2021 = Player.objects.create(
        first="Brooks",
        last="Ey",
        hsgrad_year=2021,
        last_spring=2024,
        bats="right",
        throws="right",
    )
    jm2019 = Player.objects.create(
        first="Jack",
        last="Moffitt",
        hsgrad_year=2019,
        last_spring=2025,
        bats="right",
        throws="right",
    )
    gh2024 = Player.objects.create(
        first="Grant",
        last="Hollister",
        hsgrad_year=2024,
        last_spring=2028,
        bats="left",
        throws="right",
    )
    PlayerObj = namedtuple(
        "PlayerOnj", 
        "dt2022 br2022 aw2023 nm2021 be2021 jm2019 gh2024"
    )
    return PlayerObj(
        dt2022=dt2022,
        br2022=br2022,
        aw2023=aw2023,
        nm2021=nm2021,
        be2021=be2021,
        jm2019=jm2019,
        gh2024=gh2024,
    )


@pytest.fixture
def transactions(client, players):
    current_tz = timezone.get_current_timezone()
    current_dt = datetime.now()
    dt_verbal = Transaction.objects.create(
        player=players.dt2022,
        trans_event="Verbal Commitment from High School",
        trans_date=datetime(year=2021, month=3, day=11, hour=12, tzinfo=current_tz),
    )
    dt_nli = Transaction.objects.create(
        player=players.dt2022,
        trans_event="National Letter of Intent Signed",
        trans_date=datetime(year=2021, month=11, day=7, hour=12, tzinfo=current_tz),
    )
    br_nli = Transaction.objects.create(
        player=players.br2022,
        trans_event="National Letter of Intent Signed",
        trans_date=datetime(year=2021, month=11, day=7, hour=12, tzinfo=current_tz),
    )
    nm_verbal = Transaction.objects.create(
        player=players.nm2021,
        trans_event="Verbal Commitment from College",
        trans_date=datetime(year=2023, month=11, day=7, hour=12, tzinfo=current_tz),
    )
    aw_nli = Transaction.objects.create(
        player=players.aw2023,
        trans_event="National Letter of Intent Signed", # need to aling with current choices
        trans_date=datetime(year=2022, month=11, day=7, hour=12, tzinfo=current_tz),
    )
    be_portal = Transaction.objects.create(
        player=players.be2021,
        trans_event="Entered Transfer Portal",
        trans_date=date(current_dt.year, current_dt.month, current_dt.day)
    )
    jm_verb_port = Transaction.objects.create(
        player=players.jm2019,
        trans_event="Verbal Commitment from College",
        trans_date=date(2023, 7, 1)
    )
    gh_verbal = Transaction.objects.create(
        player=players.gh2024,
        trans_event = "Verbal Commitment from High School",
        trans_date=date(year=2022, month=5, day=11),
    )
    TransObj = namedtuple(
        "TransObj", 
        "dt_verbal dt_nli be_portal br_nli nm_verbal aw_nli jm_verb_port gh_verbal"
    )
    return TransObj(
        dt_verbal=dt_verbal,
        dt_nli=dt_nli,
        be_portal=be_portal,
        br_nli=br_nli,
        nm_verbal=nm_verbal,
        aw_nli=aw_nli,
        jm_verb_port=jm_verb_port,
        gh_verbal=gh_verbal,
    )


@pytest.fixture
def trans_ly_set(client, players_last_year_set):
    current_tz = timezone.get_current_timezone()
    current_dt = datetime.now()
    dt_verbal = Transaction.objects.create(
        player=players_last_year_set.dt2022,
        trans_event="Verbal Commitment from High School",
        trans_date=datetime(year=2021, month=3, day=11, hour=12, tzinfo=current_tz),
    )
    dt_nli = Transaction.objects.create(
        player=players_last_year_set.dt2022,
        trans_event="National Letter of Intent Signed",
        trans_date=date(year=2021, month=11, day=7),
    )
    br_nli = Transaction.objects.create(
        player=players_last_year_set.br2022,
        trans_event="National Letter of Intent Signed",
        trans_date=datetime(year=2021, month=11, day=7, hour=12, tzinfo=current_tz),
    )
    nm_verbal = Transaction.objects.create(
        player=players_last_year_set.nm2021,
        trans_event="Verbal Commitment from College",
        trans_date=datetime(year=2023, month=11, day=7, hour=12, tzinfo=current_tz),
    )
    aw_nli = Transaction.objects.create(
        player=players_last_year_set.aw2023,
        trans_event="National Letter of Intent Signed", # need to aling with current choices
        trans_date=datetime(year=2022, month=11, day=7, hour=12, tzinfo=current_tz),
    )
    be_portal = Transaction.objects.create(
        player=players_last_year_set.be2021,
        trans_event="Entered Transfer Portal",
        trans_date=date(current_dt.year, current_dt.month, current_dt.day)
    )
    jm_verb_port = Transaction.objects.create(
        player=players_last_year_set.jm2019,
        trans_event="Verbal Commitment from College",
        trans_date=date(2023, 7, 1)
    )
    gh_verbal = Transaction.objects.create(
        player=players_last_year_set.gh2024,
        trans_event = "Verbal Commitment from High School",
        trans_date=date(year=2022, month=5, day=11),
    )
    TransObj = namedtuple(
        "TransObj", 
        "dt_verbal dt_nli be_portal br_nli nm_verbal aw_nli jm_verb_port gh_verbal"
    )
    return TransObj(
        dt_verbal=dt_verbal,
        dt_nli=dt_nli,
        be_portal=be_portal,
        nm_verbal=nm_verbal,
        aw_nli=aw_nli,
        br_nli=br_nli,
        jm_verb_port=jm_verb_port,
        gh_verbal=gh_verbal,
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
    nm_2022 = AnnualRoster.objects.create(
        spring_year=2022,
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
    jm_2024 = AnnualRoster.objects.create(
        spring_year=2024,
        status="Spring Roster",
        player=players.jm2019,
        team=teams.indiana,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_2023 = AnnualRoster.objects.create(
        spring_year=2023,
        status="Spring Roster",
        player=players.jm2019,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_2022 = AnnualRoster.objects.create(
        spring_year=2022,
        status="On Spring Roster but did not play",
        player=players.jm2019,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_2021 = AnnualRoster.objects.create(
        spring_year=2021,
        status="Redshirt with clock extension - Medical",
        player=players.jm2019,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )
    jm_2020 = AnnualRoster.objects.create(
        spring_year=2020,
        status="On Spring Roster but did not play",
        player=players.jm2019,
        team=teams.duke,
        jersey=16,
        primary_position="Pitcher",
    )      
    AnnualRosterObj = namedtuple(
        "AnnualRosterObj",
        "dt_2023 dt_2024 nm_2022 nm_2023 nm_2024 br_2023 jm2020 jm2021 jm2022 jm2023 jm2024"
    )
    return AnnualRosterObj(
        dt_2023=dt_2023,
        dt_2024=dt_2024,
        nm_2022=nm_2022,
        nm_2023=nm_2023,
        nm_2024=nm_2024,
        br_2023=br_2023,
        jm2020=jm_2020,
        jm2021=jm_2021,
        jm2022=jm_2022,
        jm2023=jm_2023,
        jm2024=jm_2024,
    )


@pytest.fixture
def mlb_draft_date(client):
    draft_2024 = MLBDraftDate.objects.create(
        fall_year=2024,
        latest_birthdate=date(2003, 8, 1),
        latest_draft_day=date(2024, 7, 16),
        signing_deadline=date(2024, 7, 25),
    )
    MLBDraftDateObj = namedtuple(
        "MLBDraftDateObj",
        "draft_2024"
    )
    return MLBDraftDateObj(
        draft_2024=draft_2024,
    )