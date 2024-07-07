import pytest

from collections import namedtuple
from django.utils import timezone
from datetime import datetime, date

from player_tracking.models import Transaction
from .players import players


@pytest.fixture
def transactions(players):
    current_tz = timezone.get_current_timezone()
    current_dt = datetime.now()
    dt_verbal = Transaction.objects.create(
        player=players.dt2022,
        trans_event="Verbal Commitment from High School",
        trans_date=date(year=2021, month=3, day=11),
    )
    dt_nli = Transaction.objects.create(
        player=players.dt2022,
        trans_event="National Letter of Intent Signed",
        trans_date=date(year=2021, month=11, day=7),
    )
    br_nli = Transaction.objects.create(
        player=players.br2022,
        trans_event="National Letter of Intent Signed",
        trans_date=date(year=2021, month=11, day=7),
    )
    nm_verbal = Transaction.objects.create(
        player=players.nm2021,
        trans_event="Verbal Commitment from College",
        trans_date=date(year=2023, month=11, day=7),
    )
    nm_combine = Transaction.objects.create(
        player=players.nm2021,
        trans_event="Attending MLB Draft Combine",
        trans_date=date(year=2024, month=6, day=14),
    )
    aw_nli = Transaction.objects.create(
        player=players.aw2023,
        trans_event="National Letter of Intent Signed",  # need to aling with current choices
        trans_date=date(year=2022, month=11, day=7),
    )
    be_portal = Transaction.objects.create(
        player=players.be2021,
        trans_event="Entered Transfer Portal",
        trans_date=date(current_dt.year, current_dt.month, current_dt.day),
    )
    jm_verb_port = Transaction.objects.create(
        player=players.jm2019,
        trans_event="Verbal Commitment from College",
        trans_date=date(2023, 7, 1),
    )
    gh_verbal = Transaction.objects.create(
        player=players.gh2024,
        trans_event="Verbal Commitment from High School",
        trans_date=date(year=2022, month=3, day=11),
    )
    gh_combine = Transaction.objects.create(
        player=players.gh2024,
        trans_event="Attending MLB Draft Combine",
        trans_date=date(year=2024, month=6, day=14),
    )
    cg_port = Transaction.objects.create(
        player=players.cg2020,
        trans_event="Verbal Commitment from College",
        trans_date=date(2024, 6, 14),
    )
    nb_verbal = Transaction.objects.create(
        player=players.nb2023,
        trans_event="Verbal Commitment from High School",
        trans_date=date(year=2022, month=3, day=17),
    )
    nb_diff_role = Transaction.objects.create(
        player=players.nb2023,
        trans_event="Not playing but with the program in another role",
        trans_date=date(year=2024, month=2, day=15),
    )
    TransObj = namedtuple(
        "TransObj",
        "dt_verbal dt_nli be_portal br_nli nm_verbal nm_combine aw_nli jm_verb_port gh_verbal gh_combine cg_port nb_verbal nb_diff_role",
    )
    return TransObj(
        dt_verbal=dt_verbal,
        dt_nli=dt_nli,
        be_portal=be_portal,
        br_nli=br_nli,
        nm_verbal=nm_verbal,
        nm_combine=nm_combine,
        aw_nli=aw_nli,
        jm_verb_port=jm_verb_port,
        gh_verbal=gh_verbal,
        gh_combine=gh_combine,
        cg_port=cg_port,
        nb_verbal=nb_verbal,
        nb_diff_role=nb_diff_role
    )
