from decimal import Decimal
from typing import FrozenSet, List, Sequence, Tuple

from django.db.models import Q, Sum, Value, DecimalField
from django.db.models.functions import Coalesce

from conference import models as conf_models

HOME_WIN_WEIGHT = Decimal("0.7")
HOME_LOSS_WEIGHT = Decimal("1.3")
ROAD_WIN_WEIGHT = Decimal("1.3")
ROAD_LOSS_WEIGHT = Decimal("0.7")
ZERO = Decimal("0")
DECIMAL_FIELD = DecimalField(max_digits=10, decimal_places=1)


def as_decimal(value) -> Decimal:
    if value is None:
        return ZERO
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def pair_series_split(
    team_a_pk: int, team_b_pk: int, spring_year: int
) -> Tuple[Decimal, Decimal, Decimal, Decimal]:
    """
    Return team_a's home wins/home losses/away wins/away losses against team_b
    in the requested spring_year.
    """
    home_series = conf_models.ConfSeries.objects.filter(
        home_team_id=team_a_pk,
        away_team_id=team_b_pk,
        start_date__year=spring_year,
    ).aggregate(
        a_home_wins=Coalesce(
            Sum("home_wins"),
            Value(ZERO, output_field=DECIMAL_FIELD),
            output_field=DECIMAL_FIELD,
        ),
        a_home_losses=Coalesce(
            Sum("away_wins"),
            Value(ZERO, output_field=DECIMAL_FIELD),
            output_field=DECIMAL_FIELD,
        ),
    )

    away_series = conf_models.ConfSeries.objects.filter(
        away_team_id=team_a_pk,
        home_team_id=team_b_pk,
        start_date__year=spring_year,
    ).aggregate(
        a_away_wins=Coalesce(
            Sum("away_wins"),
            Value(ZERO, output_field=DECIMAL_FIELD),
            output_field=DECIMAL_FIELD,
        ),
        a_away_losses=Coalesce(
            Sum("home_wins"),
            Value(ZERO, output_field=DECIMAL_FIELD),
            output_field=DECIMAL_FIELD,
        ),
    )

    return (
        as_decimal(home_series["a_home_wins"]),
        as_decimal(home_series["a_home_losses"]),
        as_decimal(away_series["a_away_wins"]),
        as_decimal(away_series["a_away_losses"]),
    )


def pair_series_between(
    team_a_pk: int, team_b_pk: int, spring_year: int
) -> Tuple[Decimal, Decimal, Decimal]:
    """
    Return team_a's wins/losses/games against team_b in spring_year.
    """
    home_wins, home_losses, away_wins, away_losses = pair_series_split(
        team_a_pk, team_b_pk, spring_year
    )
    wins = home_wins + away_wins
    losses = home_losses + away_losses
    games = wins + losses
    return wins, losses, games


def get_played_opponents_for_team(
    team_pk: int,
    spring_year: int,
    allowed_team_ids: FrozenSet[int],
) -> Tuple[int, ...]:
    """
    Return opponents in the allowed conference set that team_pk has actually played
    in spring_year. Scheduled-but-unplayed series are ignored.
    """
    home_opps = conf_models.ConfSeries.objects.filter(
        home_team_id=team_pk,
        start_date__year=spring_year,
    ).filter(
        Q(home_wins__gt=0) | Q(away_wins__gt=0)
    ).values_list("away_team_id", flat=True)

    away_opps = conf_models.ConfSeries.objects.filter(
        away_team_id=team_pk,
        start_date__year=spring_year,
    ).filter(
        Q(home_wins__gt=0) | Q(away_wins__gt=0)
    ).values_list("home_team_id", flat=True)

    opponents = sorted(
        {
            int(opp)
            for opp in list(home_opps) + list(away_opps)
            if int(opp) in allowed_team_ids and int(opp) != team_pk
        }
    )
    return tuple(opponents)


def calculate_win_percentage(wins: Decimal, losses: Decimal) -> Decimal:
    total = wins + losses
    if total == 0:
        return ZERO
    return wins / total


def get_raw_record_for_team(
    team_pk: int,
    spring_year: int,
    allowed_team_ids: FrozenSet[int],
    exclude_team_ids: FrozenSet[int] = frozenset(),
) -> Tuple[Decimal, Decimal]:
    """
    Raw conference record for team_pk against allowed opponents, excluding any
    team ids passed in exclude_team_ids.
    """
    wins = ZERO
    losses = ZERO

    for opp in get_played_opponents_for_team(team_pk, spring_year, allowed_team_ids):
        if opp in exclude_team_ids:
            continue

        opp_wins, opp_losses, games = pair_series_between(team_pk, opp, spring_year)
        if games == 0:
            continue

        wins += opp_wins
        losses += opp_losses

    return wins, losses


def get_adjusted_record_for_team(
    team_pk: int,
    spring_year: int,
    allowed_team_ids: FrozenSet[int],
    exclude_team_ids: FrozenSet[int] = frozenset(),
) -> Tuple[Decimal, Decimal]:
    """
    Conference record with home/road weights applied.
    Home win = 0.7 wins, home loss = 1.3 losses.
    Road win = 1.3 wins, road loss = 0.7 losses.
    """
    wins = ZERO
    losses = ZERO

    for opp in get_played_opponents_for_team(team_pk, spring_year, allowed_team_ids):
        if opp in exclude_team_ids:
            continue

        home_wins, home_losses, away_wins, away_losses = pair_series_split(
            team_pk, opp, spring_year
        )

        wins += (home_wins * HOME_WIN_WEIGHT) + (away_wins * ROAD_WIN_WEIGHT)
        losses += (home_losses * HOME_LOSS_WEIGHT) + (away_losses * ROAD_LOSS_WEIGHT)

    return wins, losses


def calculate_opponents_record_for_team(
    team_pk: int,
    spring_year: int,
    allowed_team_ids: FrozenSet[int],
    exclude_team_pk: int,
) -> Tuple[Decimal, Decimal]:
    """
    The b) component:
    weighted conference record of team_pk's opponents, excluding games versus
    exclude_team_pk.
    """
    wins = ZERO
    losses = ZERO

    for opponent_pk in get_played_opponents_for_team(
        team_pk, spring_year, allowed_team_ids
    ):
        if opponent_pk == exclude_team_pk:
            continue

        _, _, games = pair_series_between(team_pk, opponent_pk, spring_year)
        if games == 0:
            continue

        opponent_wins, opponent_losses = get_raw_record_for_team(
            opponent_pk,
            spring_year,
            allowed_team_ids,
            exclude_team_ids=frozenset({exclude_team_pk}),
        )
        wins += opponent_wins
        losses += opponent_losses

    return wins, losses


def calculate_opponents_opponents_record_for_team(
    team_pk: int,
    spring_year: int,
    allowed_team_ids: FrozenSet[int],
    exclude_team_pk: int,
) -> Tuple[Decimal, Decimal]:
    """
    The c) component:
    weighted conference record of team_pk's opponents' opponents, excluding
    games versus exclude_team_pk at every step.
    """
    wins = ZERO
    losses = ZERO

    for opponent_pk in get_played_opponents_for_team(
        team_pk, spring_year, allowed_team_ids
    ):
        if opponent_pk == exclude_team_pk:
            continue

        _, _, games = pair_series_between(team_pk, opponent_pk, spring_year)
        if games == 0:
            continue

        opponent_wins, opponent_losses = calculate_opponents_record_for_team(
            opponent_pk,
            spring_year,
            allowed_team_ids,
            exclude_team_pk=exclude_team_pk,
        )
        wins += opponent_wins
        losses += opponent_losses

    return wins, losses


def build_crpi_rows(teams: Sequence, spring_year: int) -> List[dict]:
    """
    Build the ranked cRPI rows for template rendering.
    """
    allowed_team_ids = frozenset(team.pk for team in teams)
    rows: List[dict] = []

    for team in teams:
        conference_wins, conference_losses = get_raw_record_for_team(
            team.pk, spring_year, allowed_team_ids
        )
        adjusted_wins, adjusted_losses = get_adjusted_record_for_team(
            team.pk, spring_year, allowed_team_ids
        )
        opponent_wins, opponent_losses = calculate_opponents_record_for_team(
            team.pk,
            spring_year,
            allowed_team_ids,
            exclude_team_pk=team.pk,
        )
        opp_opp_wins, opp_opp_losses = calculate_opponents_opponents_record_for_team(
            team.pk,
            spring_year,
            allowed_team_ids,
            exclude_team_pk=team.pk,
        )

        conference_win_pct = calculate_win_percentage(conference_wins, conference_losses)
        adjusted_win_pct = calculate_win_percentage(adjusted_wins, adjusted_losses)
        opponent_win_pct = calculate_win_percentage(opponent_wins, opponent_losses)
        opp_opp_win_pct = calculate_win_percentage(opp_opp_wins, opp_opp_losses)

        crpi = (
            (adjusted_win_pct * Decimal("0.25"))
            + (opponent_win_pct * Decimal("0.50"))
            + (opp_opp_win_pct * Decimal("0.25"))
        )

        rows.append(
            {
                "team": team,
                "team_name": team.team_name,
                "conference_wins": conference_wins,
                "conference_losses": conference_losses,
                "conference_win_pct": conference_win_pct,
                "adjusted_wins": adjusted_wins,
                "adjusted_losses": adjusted_losses,
                "adjusted_win_pct": adjusted_win_pct,
                "opponent_wins": opponent_wins,
                "opponent_losses": opponent_losses,
                "opponent_win_pct": opponent_win_pct,
                "opponents_opponents_wins": opp_opp_wins,
                "opponents_opponents_losses": opp_opp_losses,
                "opponents_opponents_win_pct": opp_opp_win_pct,
                "crpi": crpi,
            }
        )

    rows.sort(key=lambda row: (-row["crpi"], row["team_name"].casefold()))
    return rows