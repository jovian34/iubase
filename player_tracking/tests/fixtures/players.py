import pytest

from collections import namedtuple
from datetime import date

from player_tracking.models import Player


this_year = date.today().year


@pytest.fixture
def players():
    jake_stadler = Player.objects.create(
        first="Jake",
        last="Stadler",
        hsgrad_year=this_year - 3,
        birthdate=date(this_year - 22, 4, 30),
        bats="Left",
        throws="Right",
    )
    ryan_kraft = Player.objects.create(
        first="Ryan",
        last="Kraft",
        hsgrad_year=this_year - 3,
        birthdate=date(this_year - 22, 4, 30),
        bats="Left",
        throws="Left",
    )
    devin_taylor = Player.objects.create(
        first="Devin",
        last="Taylor",
        hsgrad_year=this_year - 2,
        birthdate=date(this_year - 20, 4, 30),
        bats="Left",
        throws="Left",
        headshot="https://iubase.com/wp-content/uploads/2023/03/Taylor-still_00001-2.jpg",
        action_shot="https://live.staticflickr.com/65535/54014518896_5c58571da6_o.jpg",
    )
    brayden_risedorph = Player.objects.create(
        first="Brayden",
        last="Risedorph",
        hsgrad_year=this_year - 2,
        birthdate=date(this_year - 21, 7, 30),
        bats="Right",
        throws="Right",
    )
    andrew_wiggins = Player.objects.create(
        first="Andrew",
        last="Wiggins",
        hsgrad_year=this_year - 1,
        bats="Left",
        throws="Right",
    )
    nick_mitchell = Player.objects.create(
        first="Nick",
        last="Mitchell",
        hsgrad_year=this_year - 3,
        bats="Left",
        throws="Right",
    )
    brooks_ey = Player.objects.create(
        first="Brooks",
        last="Ey",
        hsgrad_year=this_year - 3,
        bats="Right",
        throws="Right",
    )
    jack_moffitt = Player.objects.create(
        first="Jack",
        last="Moffitt",
        hsgrad_year=this_year - 5,
        bats="Right",
        throws="Right",
    )
    grant_hollister = Player.objects.create(
        first="Grant",
        last="Hollister",
        hsgrad_year=this_year,
        bats="Left",
        throws="Right",
    )
    cole_gilley = Player.objects.create(
        first="Cole",
        last="Gilley",
        hsgrad_year=this_year - 4,
        bats="Right",
        throws="Right",
    )
    nate_ball = Player.objects.create(
        first="Nathan",
        last="Ball",
        hsgrad_year=this_year - 1,
        bats="Right",
        throws="Right",
    )
    holton_compton = Player.objects.create(
        first="Holton",
        last="Compton",
        hsgrad_year=this_year - 2,
        birthdate=date(this_year - 21, 7, 30),
        bats="Right",
        throws="Right",
    )
    xavier_carrera = Player.objects.create(
        first="Xavier",
        last="Carrera",
        hsgrad_year=this_year + 1,
        bats="Right",
        throws="Right",
    )
    owen_ten_oever = Player.objects.create(
        first="Owen",
        last="ten Oever",
        hsgrad_year=this_year + 1,
        bats="Right",
        throws="Right",
    )
    PlayerObj = namedtuple(
        "PlayerObj",
        "jake_stadler ryan_kraft devin_taylor brayden_risedorph andrew_wiggins nick_mitchell brooks_ey jack_moffitt grant_hollister cole_gilley nate_ball holton_compton xavier_carrera owen_ten_oever",
    )
    return PlayerObj(
        jake_stadler=jake_stadler,
        ryan_kraft=ryan_kraft,
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
        xavier_carrera=xavier_carrera,
        owen_ten_oever=owen_ten_oever,
    )
