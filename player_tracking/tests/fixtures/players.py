import pytest

from collections import namedtuple
from datetime import date

from player_tracking.models import Player


this_year = date.today().year


@pytest.fixture
def players():
    devin_taylor = Player.objects.create(
        first="Devin", last="Taylor", hsgrad_year=this_year - 2, bats="left", throws="left"
    )
    brayden_risedorph = Player.objects.create(
        first="Brayden",
        last="Risedorph",
        hsgrad_year=this_year - 2,
        birthdate=date(this_year - 21, 7, 30),
        bats="right",
        throws="right",
    )
    andrew_wiggins = Player.objects.create(
        first="Andrew", last="Wiggings", hsgrad_year=this_year -1, bats="left", throws="right"
    )
    nick_mitchell = Player.objects.create(
        first="Nick",
        last="Mitchell",
        hsgrad_year=this_year - 3,
        bats="left",
        throws="right",
    )
    brooks_ey = Player.objects.create(
        first="Brooks",
        last="Ey",
        hsgrad_year=this_year - 3,
        bats="right",
        throws="right",
    )
    jack_moffitt = Player.objects.create(
        first="Jack",
        last="Moffitt",
        hsgrad_year=this_year - 5,
        bats="right",
        throws="right",
    )
    grant_hollister = Player.objects.create(
        first="Grant",
        last="Hollister",
        hsgrad_year=this_year,
        bats="left",
        throws="right",
    )
    cole_gilley = Player.objects.create(
        first="Cole",
        last="Gilley",
        hsgrad_year=this_year - 4,
        bats="right",
        throws="right",
    )
    nate_ball = Player.objects.create(
        first="Nathan",
        last="Ball",
        hsgrad_year=this_year - 1,
        bats="right",
        throws="right",
    )
    holton_compton = Player.objects.create(
        first="Holton",
        last="Compton",
        hsgrad_year=this_year - 2,
        bats="right",
        throws="right",
    )
    PlayerObj = namedtuple(
        "PlayerOnj", "devin_taylor brayden_risedorph andrew_wiggins nick_mitchell brooks_ey jack_moffitt grant_hollister cole_gilley nate_ball holton_compton"
    )
    return PlayerObj(
        devin_taylor=devin_taylor,
        brayden_risedorph=brayden_risedorph,
        andrew_wiggins=andrew_wiggins,
        nick_mitchell=nick_mitchell,
        brooks_ey=brooks_ey,
        jack_moffitt=jack_moffitt,
        grant_hollister=grant_hollister,
        cole_gilley=cole_gilley,
        nate_ball=nate_ball,
        holton_compton=holton_compton,
    )
