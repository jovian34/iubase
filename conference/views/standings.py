# conference/views/standings.py
"""
Standings view with tie-breaking.

Rules implemented (in order) for groups of teams with equal conference win_pct:
1) If all tied teams have played each other, order by head-to-head win_pct among tied teams.
2) If a team has played *all* other teams in the tied group and has a strictly
   better (or strictly worse) pct vs the tied group, award top (or bottom) spot.
3) Order by winning pct vs common opponents (opponents outside the tied group
   that are common to all tied teams).
4) Order by rpi_rank (ascending: lower = better).

Any remaining ties after applying a rule are re-processed starting at rule 1.

This version annotates each team dict with 'tiebreaker' describing which rule
was used to separate/place that team (or None).
"""

from decimal import Decimal
from collections import defaultdict
from typing import List, Tuple, Dict, Set

from django import shortcuts
from django.db.models import (
    Sum, OuterRef, Subquery, Value, DecimalField, FloatField, Case, When, Q,
    F, ExpressionWrapper,
)
from django.db.models.functions import Coalesce, Cast

from conference import models as conf_models
from live_game_blog import models as lgb_models
from conference.views import conf_year

# Small float tolerance for comparisons
EPS = 1e-9


def _get_spring_year():
    # reuse existing util if you have it; conf_year.get_spring_year() exists in project
    try:
        return conf_year.get_spring_year()
    except Exception:
        import datetime
        sy = datetime.date.today().year
        if datetime.date.today().month > 8:
            return sy + 1
        return sy


def _annotated_teams_queryset(spring_year):
    """
    Produce a queryset annotated with home_wins/away_wins/home_losses/away_losses,
    wins, losses, win_pct, rpi_rank — similar to the original implementation.
    """
    # team rpi subquery
    rpi_subquery = conf_models.TeamRpi.objects.filter(
        team=OuterRef('pk'),
        spring_year=spring_year
    ).values('rpi_rank')[:1]

    # per-team home/away wins & losses via subqueries
    home_wins_sq = conf_models.ConfSeries.objects.filter(
        home_team=OuterRef('pk'),
        start_date__year=spring_year
    ).values('home_team').annotate(total=Sum('home_wins')).values('total')[:1]

    away_wins_sq = conf_models.ConfSeries.objects.filter(
        away_team=OuterRef('pk'),
        start_date__year=spring_year
    ).values('away_team').annotate(total=Sum('away_wins')).values('total')[:1]

    home_losses_sq = conf_models.ConfSeries.objects.filter(
        home_team=OuterRef('pk'),
        start_date__year=spring_year
    ).values('home_team').annotate(total=Sum('away_wins')).values('total')[:1]

    away_losses_sq = conf_models.ConfSeries.objects.filter(
        away_team=OuterRef('pk'),
        start_date__year=spring_year
    ).values('away_team').annotate(total=Sum('home_wins')).values('total')[:1]

    zero_decimal = Value(Decimal('0'), output_field=DecimalField())

    teams_qs = lgb_models.Team.objects.all()

    teams_qs = teams_qs.annotate(
        home_wins=Coalesce(Subquery(home_wins_sq), zero_decimal),
        away_wins=Coalesce(Subquery(away_wins_sq), zero_decimal),
        home_losses=Coalesce(Subquery(home_losses_sq), zero_decimal),
        away_losses=Coalesce(Subquery(away_losses_sq), zero_decimal),
        rpi_rank=Subquery(rpi_subquery),
    ).annotate(
        wins=F('home_wins') + F('away_wins'),
        losses=F('home_losses') + F('away_losses'),
    ).annotate(
        win_pct=Case(
            When(Q(wins__gt=0) | Q(losses__gt=0),
                 then=ExpressionWrapper(
                     Cast(F('wins'), FloatField()) /
                     Cast((F('wins') + F('losses')), FloatField()),
                     output_field=FloatField()
                 )
                 ),
            default=Value(0.0),
            output_field=FloatField()
        )
    )

    return teams_qs


# ---------- Helper: access ConfSeries results for pairwise and vs-opponent stats ----------

def _pair_series_between(a_pk: int, b_pk: int, spring_year: int):
    """
    Return aggregated (a_wins, a_losses, games) for team with pk a_pk
    against team with pk b_pk in spring_year.
    Uses ConfSeries where home/away fields indicate which is which.
    """
    # a as home, b as away
    home_series = conf_models.ConfSeries.objects.filter(
        home_team_id=a_pk, away_team_id=b_pk, start_date__year=spring_year
    ).aggregate(
        a_home_wins=Coalesce(Sum('home_wins'), Value(Decimal('0')), output_field=DecimalField()),
        a_home_losses=Coalesce(Sum('away_wins'), Value(Decimal('0')), output_field=DecimalField()),
    )
    # a as away, b as home
    away_series = conf_models.ConfSeries.objects.filter(
        away_team_id=a_pk, home_team_id=b_pk, start_date__year=spring_year
    ).aggregate(
        a_away_wins=Coalesce(Sum('away_wins'), Value(Decimal('0')), output_field=DecimalField()),
        a_away_losses=Coalesce(Sum('home_wins'), Value(Decimal('0')), output_field=DecimalField()),
    )

    a_wins = Decimal(home_series['a_home_wins']) + Decimal(away_series['a_away_wins'])
    a_losses = Decimal(home_series['a_home_losses']) + Decimal(away_series['a_away_losses'])
    games = a_wins + a_losses

    return a_wins, a_losses, games


def _aggregate_vs_group(team_pk: int, group_pks: Set[int], spring_year: int) -> Tuple[Decimal, Decimal]:
    """
    Sum wins and losses for team_pk vs all teams in group_pks (excluding self).
    Returns (wins, losses) as Decimal.
    """
    wins = Decimal('0')
    losses = Decimal('0')
    for opp in group_pks:
        if opp == team_pk:
            continue
        a_wins, a_losses, games = _pair_series_between(team_pk, opp, spring_year)
        wins += a_wins
        losses += a_losses
    return wins, losses


def _played_pairwise(team_a_pk: int, team_b_pk: int, spring_year: int) -> bool:
    """
    True if there exists at least one ConfSeries between team_a and team_b in spring_year.
    """
    return conf_models.ConfSeries.objects.filter(
        (Q(home_team_id=team_a_pk) & Q(away_team_id=team_b_pk)) |
        (Q(home_team_id=team_b_pk) & Q(away_team_id=team_a_pk)),
        start_date__year=spring_year
    ).exists()


def _opponents_for_team(team_pk: int, spring_year: int) -> Set[int]:
    """
    Return set of opponent team PKs that team_pk has any ConfSeries vs in spring_year.
    """
    home_opps = conf_models.ConfSeries.objects.filter(
        home_team_id=team_pk, start_date__year=spring_year
    ).values_list('away_team_id', flat=True)
    away_opps = conf_models.ConfSeries.objects.filter(
        away_team_id=team_pk, start_date__year=spring_year
    ).values_list('home_team_id', flat=True)
    return set(list(home_opps) + list(away_opps))


def _wins_losses_vs_opponents(team_pk: int, opponent_pks: Set[int], spring_year: int) -> Tuple[Decimal, Decimal]:
    """
    Sum wins/losses for team_pk vs the list of opponent_pks (opponents are outside the tied group).
    """
    wins = Decimal('0')
    losses = Decimal('0')
    for opp in opponent_pks:
        a_wins, a_losses, games = _pair_series_between(team_pk, opp, spring_year)
        wins += a_wins
        losses += a_losses
    return wins, losses


# ---------- Tie resolution core ----------

def _pct_from_wl(wins: Decimal, losses: Decimal) -> float:
    total = wins + losses
    if total == 0:
        return 0.0
    return float(wins / total)


def resolve_ties(team_list: List[dict], spring_year: int) -> List[dict]:
    """
    team_list: list of dicts with at least keys: 'pk', 'team_name', 'wins', 'losses', 'win_pct', 'rpi_rank'
    Returns list ordered with ties resolved per rules. Each dict will also have 'tiebreaker'.
    """
    # ensure each team dict has 'tiebreaker' key
    for t in team_list:
        t.setdefault('tiebreaker', None)

    # group by primary win_pct (float). Use rounding to avoid tiny float issues.
    def key_win_pct(team):
        return round(float(team.get('win_pct', 0.0)), 8)

    # initial stable sort by win_pct desc, then rpi as stable fallback (keeps deterministic)
    team_list = sorted(team_list, key=lambda t: (-key_win_pct(t), t.get('rpi_rank') or 999999))

    result: List[dict] = []
    i = 0
    n = len(team_list)

    while i < n:
        # collect block with same win_pct
        j = i + 1
        while j < n and abs(key_win_pct(team_list[j]) - key_win_pct(team_list[i])) < EPS:
            j += 1
        block = team_list[i:j]
        if len(block) == 1:
            result.append(block[0])
            i = j
            continue

        # resolve this tied block recursively using tie-breakers
        resolved_block = _resolve_block(block, spring_year, depth=0)
        result.extend(resolved_block)
        i = j

    return result


def _resolve_block(block: List[dict], spring_year: int, depth: int = 0) -> List[dict]:
    """
    Resolve ordering for a block of tied teams (same primary win_pct).
    Returns ordered list of team dicts (fully resolved). Annotates placed teams'
    'tiebreaker' where appropriate.

    depth: recursion guard to prevent infinite loops; if exceeded, we fall back to rpi.
    """
    # Base: if only one
    if len(block) <= 1:
        return block

    # Safety guard: avoid infinite recursion by falling back to rpi after a while
    MAX_DEPTH = max(20, len(block) * 6)
    if depth > MAX_DEPTH:
        for t in block:
            t['tiebreaker'] = t.get('tiebreaker') or "rpi-fallback"
        return sorted(block, key=lambda t: (t.get('rpi_rank') if t.get('rpi_rank') is not None else 999999))

    pks = [t['pk'] for t in block]
    pks_set = set(pks)

    # ---- Rule 1: if all teams have played each other, order by head-to-head pct ----
    all_pairs_played = True
    for a in pks:
        for b in pks:
            if a == b:
                continue
            if not _played_pairwise(a, b, spring_year):
                all_pairs_played = False
                break
        if not all_pairs_played:
            break

    if all_pairs_played:
        # compute h2h pct for each team
        h2h_map = {}
        for t in block:
            wins, losses = _aggregate_vs_group(t['pk'], pks_set, spring_year)
            pct = _pct_from_wl(wins, losses)
            h2h_map[t['pk']] = (pct, wins, losses)

        # group by pct (rounded)
        groups: Dict[float, List[dict]] = defaultdict(list)
        for t in block:
            pct = round(h2h_map[t['pk']][0], 8)
            groups[pct].append(t)

        # sort pct groups descending
        sorted_pcts = sorted(groups.keys(), reverse=True)
        out: List[dict] = []
        for pct in sorted_pcts:
            grp = groups[pct]
            if len(grp) == 1:
                # this team is uniquely placed by head-to-head
                grp[0]['tiebreaker'] = grp[0].get('tiebreaker') or "tie broke by head-to-head"
                out.append(grp[0])
            else:
                # recursively resolve subgroup (go back to rule 1)
                out.extend(_resolve_block(grp, spring_year, depth=depth+1))
        return out

    # ---- Rule 2: any team played *all* other tied teams and strictly better/worse vs all of them ----
    # compute each team's pct vs group (where played count can be 0)
    pct_vs_group = {}
    played_all = {}
    for t in block:
        wins, losses = _aggregate_vs_group(t['pk'], pks_set, spring_year)
        total = wins + losses
        pct = _pct_from_wl(wins, losses)
        pct_vs_group[t['pk']] = (pct, wins, losses, total)
        # played all others if for every other pk there's at least one series
        ok = True
        for opp in pks:
            if opp == t['pk']:
                continue
            if not _played_pairwise(t['pk'], opp, spring_year):
                ok = False
                break
        played_all[t['pk']] = ok

    # Look for a team that has played all and has strictly higher pct_vs_group than every other team's pct_vs_group
    top_candidate = None
    for pk in pks:
        if not played_all.get(pk, False):
            continue
        my_pct = pct_vs_group[pk][0]
        strictly_better = True
        for other_pk in pks:
            if other_pk == pk:
                continue
            if not (my_pct > pct_vs_group[other_pk][0] + EPS):
                strictly_better = False
                break
        if strictly_better:
            top_candidate = pk
            break

    if top_candidate is not None:
        # place top_candidate first, annotate tiebreaker, then resolve remaining block
        top_team = next(t for t in block if t['pk'] == top_candidate)
        top_team['tiebreaker'] = top_team.get('tiebreaker') or "better record vs all in tied group"
        remaining = [t for t in block if t['pk'] != top_candidate]
        return [top_team] + _resolve_block(remaining, spring_year, depth=depth+1)

    # check for strict worst (played all and strictly worse than all others)
    worst_candidate = None
    for pk in pks:
        if not played_all.get(pk, False):
            continue
        my_pct = pct_vs_group[pk][0]
        strictly_worse = True
        for other_pk in pks:
            if other_pk == pk:
                continue
            if not (my_pct + EPS < pct_vs_group[other_pk][0]):
                strictly_worse = False
                break
        if strictly_worse:
            worst_candidate = pk
            break

    if worst_candidate is not None:
        worst_team = next(t for t in block if t['pk'] == worst_candidate)
        worst_team['tiebreaker'] = worst_team.get('tiebreaker') or "worse record vs all in tied group"
        remaining = [t for t in block if t['pk'] != worst_candidate]
        # put remaining resolved first, then worst at end
        return _resolve_block(remaining, spring_year, depth=depth+1) + [worst_team]

    # ---- Rule 3: rank by pct vs common opponents not in the tied group ----
    # compute each team's opponent set (excluding ties)
    opp_sets = {}
    for t in block:
        opp_sets[t['pk']] = _opponents_for_team(t['pk'], spring_year) - pks_set

    # common opponents across all tied teams
    common_opps = None
    for s in opp_sets.values():
        if common_opps is None:
            common_opps = set(s)
        else:
            common_opps &= s
    common_opps = common_opps or set()

    if common_opps:
        # compute pct vs common opponents
        common_pct_map = {}
        for t in block:
            wins, losses = _wins_losses_vs_opponents(t['pk'], common_opps, spring_year)
            pct = _pct_from_wl(wins, losses)
            common_pct_map[t['pk']] = (pct, wins, losses)

        # Group by pct (rounded) and recursively resolve ties inside each group
        groups: Dict[float, List[dict]] = defaultdict(list)
        for t in block:
            pct = round(common_pct_map[t['pk']][0], 8)
            groups[pct].append(t)
        sorted_pcts = sorted(groups.keys(), reverse=True)
        out = []
        for pct in sorted_pcts:
            grp = groups[pct]
            if len(grp) == 1:
                # uniquely placed by common-opponents
                grp[0]['tiebreaker'] = grp[0].get('tiebreaker') or "tie broke by record vs. common opponents"
                out.append(grp[0])
            else:
                out.extend(_resolve_block(grp, spring_year, depth=depth+1))
        return out

    # ---- Rule 4: rpi_rank ascending (lower rank number is better). Use big sentinel for missing rpi. ----
    # fallback deterministic ordering by rpi_rank
    def rpi_key(t):
        r = t.get('rpi_rank')
        return (r if r is not None else 999999)

    sorted_by_rpi = sorted(block, key=lambda t: rpi_key(t))
    # annotate with rpi tiebreaker if they don't already have a tiebreaker
    for t in sorted_by_rpi:
        t['tiebreaker'] = t.get('tiebreaker') or "tie broke by RPI"
    return sorted_by_rpi


def view(request, spring_year):
    # annotate teams with wins/losses/win_pct/rpi_rank
    teams_qs = _annotated_teams_queryset(spring_year)

    # Only include teams that have a TeamRpi for that season AND have wins OR losses (i.e., played)
    teams_qs = teams_qs.filter(
        rpi_rank__isnull=False
    ).filter(
        Q(wins__gt=0) | Q(losses__gt=0)
    )

    # Evaluate queryset -> list of dicts with required fields for tie resolution
    teams_list = []
    for t in teams_qs:
        teams_list.append({
            'pk': t.pk,
            'team_name': t.team_name,
            'wins': Decimal(t.wins),
            'losses': Decimal(t.losses),
            'win_pct': float(t.win_pct or 0.0),
            'rpi_rank': int(t.rpi_rank) if t.rpi_rank is not None else None,
            'obj': t,  # keep original model obj for rendering convenience
            'tiebreaker': None,
        })

    # Resolve ties and produce ordered list
    ordered = resolve_ties(teams_list, spring_year)

    # For template convenience, convert back into items similar to queryset objects:
    # attach computed fields onto the model instances (non-persistent)
    ordered_for_template = []
    for pos, entry in enumerate(ordered, start=1):
        model_obj = entry.get('obj')
        # annotate some attributes the template expects
        model_obj.computed_wins = entry['wins']
        model_obj.computed_losses = entry['losses']
        model_obj.computed_win_pct = entry['win_pct']
        model_obj.computed_rpi_rank = entry['rpi_rank']
        model_obj.standings_position = pos
        # attach the tiebreaker string (None if not applicable)
        model_obj.tie_breaker = entry.get('tiebreaker')
        ordered_for_template.append(model_obj)

    # Determine conference name for page_title:
    conference_name = "Conference"
    try:
        team_pks = [entry['pk'] for entry in teams_list]
        conf_names_qs = conf_models.ConfTeam.objects.filter(
            team_id__in=team_pks,
            spring_year=spring_year
        ).values_list('conference__name', flat=True).distinct()
        conf_names = list(conf_names_qs)
        if conf_names:
            conference_name = conf_names[0]
    except Exception:
        conference_name = "Conference"

    template_path = "conference/standings.html"
    context = {
        "page_title": f"{spring_year} B1G Standings",
        "standings": ordered_for_template,
        "spring_year": spring_year
    }
    return shortcuts.render(request, template_path, context)
