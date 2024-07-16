import pytest

from collections import namedtuple
from django.utils import timezone
from datetime import datetime, date

from player_tracking.models import Transaction
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs


@pytest.fixture
def transactions(players, prof_orgs):
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
    nm_draft = Transaction.objects.create(
        player=players.nm2021,
        trans_event="Drafted",
        trans_date=date(year=2024, month=7, day=15),
        prof_org=prof_orgs.phillies,
        draft_round=4,
    )
    aw_nli = Transaction.objects.create(
        player=players.aw2023,
        trans_event="National Letter of Intent Signed",
        trans_date=date(year=2022, month=11, day=7),
    )
    be_commit = Transaction.objects.create(
        player=players.be2021,
        trans_event="Verbal Commitment from College",
        trans_date=date(year=2023, month=7, day=15),
    )
    be_portal = Transaction.objects.create(
        player=players.be2021,
        trans_event="Entered Transfer Portal",
        trans_date=date(year=2024, month=6, day=15),
    )
    jm_verb_port = Transaction.objects.create(
        player=players.jm2019,
        trans_event="Verbal Commitment from College",
        trans_date=date(year=2023, month=7, day=1),
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
        "dt_verbal dt_nli be_commit be_portal br_nli nm_verbal nm_combine nm_draft aw_nli jm_verb_port gh_verbal gh_combine cg_port nb_verbal nb_diff_role",
    )
    return TransObj(
        dt_verbal=dt_verbal,
        dt_nli=dt_nli,
        be_commit=be_commit,
        be_portal=be_portal,
        br_nli=br_nli,
        nm_verbal=nm_verbal,
        nm_combine=nm_combine,
        nm_draft=nm_draft,
        aw_nli=aw_nli,
        jm_verb_port=jm_verb_port,
        gh_verbal=gh_verbal,
        gh_combine=gh_combine,
        cg_port=cg_port,
        nb_verbal=nb_verbal,
        nb_diff_role=nb_diff_role,
    )
