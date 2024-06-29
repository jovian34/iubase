import pytest

from collections import namedtuple
from datetime import date

from player_tracking.models import Player


@pytest.fixture
def players_last_year_set():
    dt2022 = Player.objects.create(
        first="Devin",
        last="Taylor",
        hsgrad_year=2022,
        last_spring=2026,
        bats="left",
        throws="left",
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
        throws="right",
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
    cg2020 = Player.objects.create(
        first="Cole",
        last="Gilley",
        hsgrad_year=2020,
        last_spring=2025,
        bats="right",
        throws="right",
    )
    PlayerObj = namedtuple(
        "PlayerOnj", "dt2022 br2022 aw2023 nm2021 be2021 jm2019 gh2024 cg2020"
    )
    return PlayerObj(
        dt2022=dt2022,
        br2022=br2022,
        aw2023=aw2023,
        nm2021=nm2021,
        be2021=be2021,
        jm2019=jm2019,
        gh2024=gh2024,
        cg2020=cg2020,
    )
