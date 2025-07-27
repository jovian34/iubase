import pytest

from collections import namedtuple
from django.utils import timezone
from datetime import datetime, date

from player_tracking.models import Transaction
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from live_game_blog.tests.fixtures.teams import teams


this_year = date.today().year


@pytest.fixture
def transactions(players, prof_orgs, teams):
    js_verbal = Transaction.objects.create(
        player=players.jake_stadler,
        trans_event="Verbal Commitment from College",
        trans_date=date(year=this_year - 1, month=6, day=7),
    )
    rk_verbal = Transaction.objects.create(
        player=players.ryan_kraft,
        trans_event="Verbal Commitment from High School",
        trans_date=date(year=this_year - 4, month=3, day=11),
    )
    rk_signed = Transaction.objects.create(
        player=players.ryan_kraft,
        trans_event="Signed Professional Contract - Undrafted",
        trans_date=date(year=this_year + 2, month=7, day=24),
    )
    dt_verbal = Transaction.objects.create(
        player=players.devin_taylor,
        trans_event="Verbal Commitment from High School",
        trans_date=date(year=this_year - 3, month=3, day=11),
    )
    dt_nli = Transaction.objects.create(
        player=players.devin_taylor,
        trans_event="National Letter of Intent Signed",
        trans_date=date(year=this_year - 3, month=11, day=7),
    )
    dt_draft_ranked = Transaction.objects.create(
        player=players.devin_taylor,
        trans_event="Ranked MLB Draft Prospect for Next Draft",
        trans_date=date(year=this_year - 1, month=12, day=10),
    )
    br_nli = Transaction.objects.create(
        player=players.brayden_risedorph,
        trans_event="National Letter of Intent Signed",
        trans_date=date(year=this_year - 3, month=11, day=7),
    )
    nm_verbal = Transaction.objects.create(
        player=players.nick_mitchell,
        trans_event="Verbal Commitment from College",
        trans_date=date(year=this_year - 1, month=6, day=7),
    )
    nm_combine = Transaction.objects.create(
        player=players.nick_mitchell,
        trans_event="Attending MLB Draft Combine",
        trans_date=date(year=this_year, month=6, day=14),
    )
    nm_draft = Transaction.objects.create(
        player=players.nick_mitchell,
        trans_event="Drafted",
        trans_date=date(year=this_year, month=7, day=15),
        prof_org=prof_orgs.phillies,
        draft_round=4,
        bonus_or_slot=400100,
        comment="Clarification: This pick was actually in a Competitive Balance round between the 4th and 5th rounds.",
    )
    nm_signed = Transaction.objects.create(
        player=players.nick_mitchell,
        trans_event="Signed Professional Contract",
        trans_date=date(year=this_year, month=7, day=21),
        prof_org=prof_orgs.phillies,
        bonus_or_slot=367000,
        comment="Bonus value was reported two days after signing.",
    )
    aw_nli = Transaction.objects.create(
        player=players.andrew_wiggins,
        trans_event="National Letter of Intent Signed",
        trans_date=date(year=this_year - 2, month=11, day=7),
    )
    be_commit = Transaction.objects.create(
        player=players.brooks_ey,
        trans_event="Verbal Commitment from College",
        trans_date=date(year=this_year - 1, month=7, day=15),
    )
    be_portal = Transaction.objects.create(
        player=players.brooks_ey,
        trans_event="Entered Transfer Portal",
        trans_date=date(year=this_year, month=6, day=15),
        citation="https://x.com/brooks_ey/status/1794162572117303480",
    )
    be_new_school = Transaction.objects.create(
        player=players.brooks_ey,
        trans_event="Verbal Commitment to Transfer College",
        trans_date=date(year=this_year, month=7, day=8),
        other_team=teams.duke,
    )
    jm_verb_port = Transaction.objects.create(
        player=players.jack_moffitt,
        trans_event="Verbal Commitment from College",
        trans_date=date(year=this_year - 1, month=7, day=1),
    )
    gh_verbal = Transaction.objects.create(
        player=players.grant_hollister,
        trans_event="Verbal Commitment from High School",
        primary_position="Pitcher",
        trans_date=date(year=this_year - 2, month=3, day=11),
    )
    gh_combine = Transaction.objects.create(
        player=players.grant_hollister,
        trans_event="Attending MLB Draft Combine",
        trans_date=date(year=this_year, month=6, day=14),
    )
    gh_draft = Transaction.objects.create(
        player=players.grant_hollister,
        trans_event="Drafted",
        primary_position="Pitcher",
        trans_date=date(year=this_year, month=7, day=14),
        comment="He is expected by insiders to require $500,000 to sign.",
    )
    gh_not_sign = Transaction.objects.create(
        player=players.grant_hollister,
        primary_position="Pitcher",
        trans_event="Not Signing Professional Contract",
        trans_date=date(year=this_year, month=8, day=1),
    )
    cg_port = Transaction.objects.create(
        player=players.cole_gilley,
        trans_event="Verbal Commitment from College",
        trans_date=date(year=this_year, month=6, day=14),
    )
    nb_verbal = Transaction.objects.create(
        player=players.nate_ball,
        trans_event="Verbal Commitment from High School",
        trans_date=date(year=this_year - 1, month=3, day=17),
    )
    nb_diff_role = Transaction.objects.create(
        player=players.nate_ball,
        trans_event="Not playing but with the program in another role",
        trans_date=date(year=this_year, month=2, day=15),
    )
    hc_verbal = Transaction.objects.create(
        player=players.holton_compton,
        trans_event="Verbal Commitment from College",
        primary_position="Shortstop",
        trans_date=date(year=this_year - 1, month=10, day=23),
    )
    xc_verbal = Transaction.objects.create(
        player=players.xavier_carrera,
        trans_event="Verbal Commitment from High School",
        trans_date=date(year=this_year - 1, month=8, day=6),
    )
    xc_nli = Transaction.objects.create(
        player=players.xavier_carrera,
        trans_event="National Letter of Intent Signed",
        trans_date=date(year=this_year, month=11, day=25),
    )
    gs_verbal = Transaction.objects.create(
        player=players.gibson_sinke,
        trans_event="Verbal Commitment from High School",
        trans_date=date(year=this_year - 2, month=8, day=11),
    )
    gs_decommit = Transaction.objects.create(
        player=players.gibson_sinke,
        trans_event="Decommit",
        trans_date=date.today(),
    )
    oo_verbal = Transaction.objects.create(
        player=players.owen_ten_oever,
        trans_event="Verbal Commitment from High School",
        trans_date=date(year=this_year - 1, month=8, day=11),
    )
    em_verbal = Transaction.objects.create(
        player=players.evan_mac,
        trans_event="Verbal Commitment from High School",
        trans_date=date(year=2020, month=9, day=26),
    )
    em_portal = Transaction.objects.create(
        player=players.evan_mac,
        trans_event="Entered Transfer Portal",
        trans_date=date(year=2022, month=12, day=11),
    )
    ja_verbal = Transaction.objects.create(
        player=players.jason_amalbert,
        trans_event="Verbal Commitment from High School",
        trans_date=date(year=this_year - 2, month=9, day=26),
    )
    ja_decommit = Transaction.objects.create(
        player=players.jason_amalbert,
        trans_event="Decommit",
        trans_date=date(year=this_year, month=2, day=5),
    )
    TransObj = namedtuple(
        "TransObj",
        "js_verbal rk_verbal rk_signed dt_verbal dt_nli be_commit be_portal be_new_school dt_draft_ranked br_nli nm_verbal nm_combine nm_draft nm_signed aw_nli jm_verb_port gh_verbal gh_draft gh_not_sign gh_combine cg_port nb_verbal nb_diff_role hc_verbal xc_verbal gs_verbal gs_decommit xc_nli oo_verbal em_verbal em_portal ja_verbal ja_decommit",
    )
    return TransObj(
        js_verbal=js_verbal,
        rk_verbal=rk_verbal,
        rk_signed=rk_signed,
        dt_verbal=dt_verbal,
        dt_nli=dt_nli,
        be_commit=be_commit,
        be_portal=be_portal,
        be_new_school=be_new_school,
        dt_draft_ranked=dt_draft_ranked,
        br_nli=br_nli,
        nm_verbal=nm_verbal,
        nm_combine=nm_combine,
        nm_draft=nm_draft,
        nm_signed=nm_signed,
        aw_nli=aw_nli,
        jm_verb_port=jm_verb_port,
        gh_verbal=gh_verbal,
        gh_draft=gh_draft,
        gh_combine=gh_combine,
        gh_not_sign=gh_not_sign,
        cg_port=cg_port,
        nb_verbal=nb_verbal,
        nb_diff_role=nb_diff_role,
        hc_verbal=hc_verbal,
        xc_verbal=xc_verbal,
        xc_nli=xc_nli,
        gs_verbal=gs_verbal,
        gs_decommit=gs_decommit,
        oo_verbal=oo_verbal,
        em_verbal=em_verbal,
        em_portal=em_portal,
        ja_verbal=ja_verbal,
        ja_decommit=ja_decommit,
    )
