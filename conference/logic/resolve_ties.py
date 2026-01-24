from decimal import Decimal
from collections import defaultdict
from typing import List, Tuple, Dict, Set

from django.db.models import (
    Sum,
    Value,
    DecimalField,
    Q,
)
from django.db.models.functions import Coalesce

from conference import models as conf_models

EPS = 1e-9  # Small float tolerance for comparisons


def pair_series_between(team_a_pk: int, team_b_pk: int, spring_year: int):
    # a as home, b as away
    home_series = conf_models.ConfSeries.objects.filter(
        home_team_id=team_a_pk, away_team_id=team_b_pk, start_date__year=spring_year
    ).aggregate(
        a_home_wins=Coalesce(
            Sum("home_wins"), Value(Decimal("0")), output_field=DecimalField()
        ),
        a_home_losses=Coalesce(
            Sum("away_wins"), Value(Decimal("0")), output_field=DecimalField()
        ),
    )
    # a as away, b as home
    away_series = conf_models.ConfSeries.objects.filter(
        away_team_id=team_a_pk, home_team_id=team_b_pk, start_date__year=spring_year
    ).aggregate(
        a_away_wins=Coalesce(
            Sum("away_wins"), Value(Decimal("0")), output_field=DecimalField()
        ),
        a_away_losses=Coalesce(
            Sum("home_wins"), Value(Decimal("0")), output_field=DecimalField()
        ),
    )
    a_wins = Decimal(home_series["a_home_wins"]) + Decimal(away_series["a_away_wins"])
    a_losses = Decimal(home_series["a_home_losses"]) + Decimal(
        away_series["a_away_losses"]
    )
    games = a_wins + a_losses
    return a_wins, a_losses, games


def aggregate_vs_group(
    team_pk: int, group_pks: Set[int], spring_year: int
) -> Tuple[Decimal, Decimal]:
    wins = Decimal("0")
    losses = Decimal("0")
    for opp in group_pks:
        if opp == team_pk:
            continue
        a_wins, a_losses, games = pair_series_between(team_pk, opp, spring_year)
        wins += a_wins
        losses += a_losses
    return wins, losses


def have_two_teams_played(team_a_pk: int, team_b_pk: int, spring_year: int) -> bool:
    return conf_models.ConfSeries.objects.filter(
        (Q(home_team_id=team_a_pk) & Q(away_team_id=team_b_pk))
        | (Q(home_team_id=team_b_pk) & Q(away_team_id=team_a_pk)),
        start_date__year=spring_year,
    ).exists()


def get_all_opponents_for_team(team_pk: int, spring_year: int) -> Set[int]:
    home_opps = conf_models.ConfSeries.objects.filter(
        home_team_id=team_pk, start_date__year=spring_year
    ).values_list("away_team_id", flat=True)
    away_opps = conf_models.ConfSeries.objects.filter(
        away_team_id=team_pk, start_date__year=spring_year
    ).values_list("home_team_id", flat=True)
    return set(list(home_opps) + list(away_opps))


def get_and_sum_wins_losses_vs_opponents(
    team_pk: int, opponent_pks: Set[int], spring_year: int
) -> Tuple[Decimal, Decimal]:
    wins = Decimal("0")
    losses = Decimal("0")
    for opp in opponent_pks:
        a_wins, a_losses, games = pair_series_between(team_pk, opp, spring_year)
        wins += a_wins
        losses += a_losses
    return wins, losses


def calculate_win_percentage(wins: Decimal, losses: Decimal) -> float:
    total = wins + losses
    if total == 0:
        return 0.0
    return float(wins / total)


def resolve_ties(team_list: List[dict], spring_year: int) -> List[dict]:
    for team in team_list:
        team.setdefault("tiebreaker", None)

    # group by primary win_pct (float). Use rounding to avoid tiny float issues.
    def key_win_pct(team):
        return round(float(team.get("win_pct", 0.0)), 8)

    # initial stable sort by win_pct desc, then rpi as stable fallback (keeps deterministic)
    team_list = sorted(
        team_list, key=lambda t: (-key_win_pct(t), t.get("rpi_rank") or 999999)
    )

    result: List[dict] = []
    i = 0
    num_of_teams = len(team_list)

    while i < num_of_teams:
        # collect block with same win_pct
        j = i + 1
        while (
            j < num_of_teams
            and abs(key_win_pct(team_list[j]) - key_win_pct(team_list[i])) < EPS
        ):
            j += 1
        block = team_list[i:j]
        if len(block) == 1:
            result.append(block[0])
            i = j
            continue

        # resolve this tied block recursively using tie-breakers
        resolved_block = resolve_block(block, spring_year, depth=0)
        result.extend(resolved_block)
        i = j

    return result


def resolve_block(block: List[dict], spring_year: int, depth: int = 0) -> List[dict]:
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
            t["tiebreaker"] = t.get("tiebreaker") or "tie broken by RPI"
        return sorted(
            block,
            key=lambda t: (
                t.get("rpi_rank") if t.get("rpi_rank") is not None else 999999
            ),
        )

    pks = [t["pk"] for t in block]
    pks_set = set(pks)

    # ---- Rule 1: if all teams have played each other, order by head-to-head pct ----
    all_pairs_played = True
    for a in pks:
        for b in pks:
            if a == b:
                continue
            if not have_two_teams_played(a, b, spring_year):
                all_pairs_played = False
                break
        if not all_pairs_played:
            break

    if all_pairs_played:
        # compute h2h pct for each team
        h2h_map = {}
        for t in block:
            wins, losses = aggregate_vs_group(t["pk"], pks_set, spring_year)
            pct = calculate_win_percentage(wins, losses)
            h2h_map[t["pk"]] = (pct, wins, losses)

        # group by pct (rounded)
        groups: Dict[float, List[dict]] = defaultdict(list)
        for t in block:
            pct = round(h2h_map[t["pk"]][0], 8)
            groups[pct].append(t)

        # sort pct groups descending
        sorted_pcts = sorted(groups.keys(), reverse=True)
        out: List[dict] = []
        for pct in sorted_pcts:
            grp = groups[pct]
            if len(grp) == 1:
                # this team is uniquely placed by head-to-head
                grp[0]["tiebreaker"] = (
                    grp[0].get("tiebreaker") or "tie broke by head-to-head"
                )
                out.append(grp[0])
            else:
                # recursively resolve subgroup (go back to rule 1)
                out.extend(resolve_block(grp, spring_year, depth=depth + 1))
        return out

    # ---- Rule 2: any team played *all* other tied teams and strictly better/worse vs all of them ----
    # compute each team's pct vs group (where played count can be 0)
    pct_vs_group = {}
    played_all = {}
    for t in block:
        wins, losses = aggregate_vs_group(t["pk"], pks_set, spring_year)
        total = wins + losses
        pct = calculate_win_percentage(wins, losses)
        pct_vs_group[t["pk"]] = (pct, wins, losses, total)
        # played all others if for every other pk there's at least one series
        ok = True
        for opp in pks:
            if opp == t["pk"]:
                continue
            if not have_two_teams_played(t["pk"], opp, spring_year):
                ok = False
                break
        played_all[t["pk"]] = ok

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
        top_team = next(t for t in block if t["pk"] == top_candidate)
        top_team["tiebreaker"] = (
            top_team.get("tiebreaker") or "better record vs all in tied group"
        )
        remaining = [t for t in block if t["pk"] != top_candidate]
        return [top_team] + resolve_block(remaining, spring_year, depth=depth + 1)

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
        worst_team = next(t for t in block if t["pk"] == worst_candidate)
        worst_team["tiebreaker"] = (
            worst_team.get("tiebreaker") or "worse record vs all in tied group"
        )
        remaining = [t for t in block if t["pk"] != worst_candidate]
        # put remaining resolved first, then worst at end
        return resolve_block(remaining, spring_year, depth=depth + 1) + [worst_team]

    # ---- Rule 3: rank by pct vs common opponents not in the tied group ----
    # compute each team's opponent set (excluding ties)
    opp_sets = {}
    for t in block:
        opp_sets[t["pk"]] = get_all_opponents_for_team(t["pk"], spring_year) - pks_set

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
            wins, losses = get_and_sum_wins_losses_vs_opponents(
                t["pk"], common_opps, spring_year
            )
            pct = calculate_win_percentage(wins, losses)
            common_pct_map[t["pk"]] = (pct, wins, losses)

        # Group by pct (rounded) and recursively resolve ties inside each group
        groups: Dict[float, List[dict]] = defaultdict(list)
        for t in block:
            pct = round(common_pct_map[t["pk"]][0], 8)
            groups[pct].append(t)
        sorted_pcts = sorted(groups.keys(), reverse=True)
        out = []
        for pct in sorted_pcts:
            grp = groups[pct]
            if len(grp) == 1:
                # uniquely placed by common-opponents
                grp[0]["tiebreaker"] = (
                    grp[0].get("tiebreaker")
                    or "tie broke by record vs. common opponents"
                )
                out.append(grp[0])
            else:
                out.extend(resolve_block(grp, spring_year, depth=depth + 1))
        return out

    # ---- Rule 4: rpi_rank ascending (lower rank number is better). Use big sentinel for missing rpi. ----
    # fallback deterministic ordering by rpi_rank
    def rpi_key(t):
        r = t.get("rpi_rank")
        return r if r is not None else 999999

    sorted_by_rpi = sorted(block, key=lambda t: rpi_key(t))
    # annotate with rpi tiebreaker if they don't already have a tiebreaker
    for t in sorted_by_rpi:
        t["tiebreaker"] = t.get("tiebreaker") or "tie broke by RPI"
    return sorted_by_rpi
