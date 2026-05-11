from decimal import Decimal
from collections import defaultdict
from typing import List

from conference import models as conf_models

ZERO = Decimal("0")

HOME_WIN_WEIGHT = Decimal("0.7")
HOME_LOSS_WEIGHT = Decimal("1.3")
ROAD_WIN_WEIGHT = Decimal("1.3")
ROAD_LOSS_WEIGHT = Decimal("0.7")


def calculate_win_percentage(wins: Decimal, losses: Decimal) -> Decimal:
    total = wins + losses
    if total == 0:
        return ZERO
    return wins / total


def build_crpi_rows(teams, spring_year: int) -> List[dict]:
    """
    Optimized cRPI calculation:
    - Single DB query
    - All math in memory
    """

    # --------------------------------------------------
    # 1. LOAD ALL SERIES (ONLY DB QUERY)
    # --------------------------------------------------
    all_series = list(
        conf_models.ConfSeries.objects.filter(start_date__year=spring_year)
    )

    team_ids = {team.pk for team in teams}

    # --------------------------------------------------
    # 2. BUILD LOOKUPS
    # --------------------------------------------------
    pair_data = defaultdict(lambda: {"wins": ZERO, "losses": ZERO})

    # directional (home/away) for adjusted calc
    pair_split = defaultdict(
        lambda: {"home_wins": ZERO, "home_losses": ZERO, "away_wins": ZERO, "away_losses": ZERO}
    )

    for s in all_series:
        home = s.home_team_id
        away = s.away_team_id

        if home not in team_ids or away not in team_ids:
            continue

        home_wins = Decimal(s.home_wins or 0)
        away_wins = Decimal(s.away_wins or 0)

        if home_wins + away_wins == 0:
            continue  # ignore unplayed series

        # aggregate pair data
        pair_data[(home, away)]["wins"] += home_wins
        pair_data[(home, away)]["losses"] += away_wins

        pair_data[(away, home)]["wins"] += away_wins
        pair_data[(away, home)]["losses"] += home_wins

        # split for home/road adjustment
        pair_split[(home, away)]["home_wins"] += home_wins
        pair_split[(home, away)]["home_losses"] += away_wins

        pair_split[(away, home)]["away_wins"] += away_wins
        pair_split[(away, home)]["away_losses"] += home_wins

    # --------------------------------------------------
    # 3. BUILD OPPONENT MAP
    # --------------------------------------------------
    opponents_map = {tid: set() for tid in team_ids}

    for (a, b), data in pair_data.items():
        if data["wins"] + data["losses"] > 0:
            opponents_map[a].add(b)

    # --------------------------------------------------
    # 4. RAW RECORDS (Pass 1)
    # --------------------------------------------------
    team_records = {}

    for tid in team_ids:
        wins = ZERO
        losses = ZERO

        for opp in opponents_map[tid]:
            rec = pair_data[(tid, opp)]
            wins += rec["wins"]
            losses += rec["losses"]

        team_records[tid] = {"wins": wins, "losses": losses}

    # --------------------------------------------------
    # 5. ADJUSTED RECORDS (home/road)
    # --------------------------------------------------
    adjusted_records = {}

    for tid in team_ids:
        wins = ZERO
        losses = ZERO

        for opp in opponents_map[tid]:
            split = pair_split[(tid, opp)]

            wins += (
                split["home_wins"] * HOME_WIN_WEIGHT
                + split["away_wins"] * ROAD_WIN_WEIGHT
            )

            losses += (
                split["home_losses"] * HOME_LOSS_WEIGHT
                + split["away_losses"] * ROAD_LOSS_WEIGHT
            )

        adjusted_records[tid] = {"wins": wins, "losses": losses}

    # --------------------------------------------------
    # 6. OPPONENT WIN % (Pass 2)
    # --------------------------------------------------
    opponent_win_pct = {}

    for tid in team_ids:
        total_w = ZERO
        total_l = ZERO

        for opp in opponents_map[tid]:
            rec = team_records[opp]

            total_w += rec["wins"]
            total_l += rec["losses"]

        opponent_win_pct[tid] = calculate_win_percentage(total_w, total_l)

    # --------------------------------------------------
    # 7. OPPONENT-OPPONENT WIN % (Pass 3)
    # --------------------------------------------------
    opponent_opponent_win_pct = {}

    for tid in team_ids:
        total_w = ZERO
        total_l = ZERO

        for opp in opponents_map[tid]:
            for opp2 in opponents_map[opp]:
                rec = team_records[opp2]

                total_w += rec["wins"]
                total_l += rec["losses"]

        opponent_opponent_win_pct[tid] = calculate_win_percentage(total_w, total_l)

    # --------------------------------------------------
    # 8. BUILD FINAL ROWS
    # --------------------------------------------------
    rows = []

    for team in teams:
        tid = team.pk

        conf_rec = team_records[tid]
        adj_rec = adjusted_records[tid]

        conf_pct = calculate_win_percentage(conf_rec["wins"], conf_rec["losses"])
        adj_pct = calculate_win_percentage(adj_rec["wins"], adj_rec["losses"])

        crpi = (
            (adj_pct * Decimal("0.25"))
            + (opponent_win_pct[tid] * Decimal("0.50"))
            + (opponent_opponent_win_pct[tid] * Decimal("0.25"))
        )

        rows.append(
            {
                "team": team,
                "team_name": team.team_name,
                "conference_wins": conf_rec["wins"],
                "conference_losses": conf_rec["losses"],
                "conference_win_pct": conf_pct,
                "adjusted_win_pct": adj_pct,
                "opponent_win_pct": opponent_win_pct[tid],
                "opponents_opponents_win_pct": opponent_opponent_win_pct[tid],
                "crpi": crpi,
            }
        )

    # --------------------------------------------------
    # 9. SORT
    # --------------------------------------------------
    rows.sort(key=lambda r: (-r["crpi"], r["team_name"].casefold()))

    return rows