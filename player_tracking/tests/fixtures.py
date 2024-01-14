import pytest

from collections import namedtuple
from django.utils import timezone
from datetime import timedelta

from player_tracking.models import Player

@pytest.fixture
def players(client):
    dt2022 = Player.objects.create(
        first = "Devin",
        last = "Taylor",
        hsgrad_year = 2022,
        bats = "left",
        throws = "left"
    )
    br2022 = Player.objects.create(
        first = "Brayden",
        last = "Risedorph",
        hsgrad_year = 2022,
        bats = "right",
        throws = "right"
    )
    aw2023 = Player.objects.create(        
        first = "Andrew",
        last = "Wiggings",
        hsgrad_year = 2023,
        bats = "left",
        throws = "right"
    )
    PlayerObj = namedtuple(
        "PlayerOnj",
        "dt2022, br2022, aw2023"
    )
    return PlayerObj(
        dt2022=dt2022,
        br2022=br2022,
        aw2023=aw2023,
    )