from player_tracking.choices import (
    AFTER,
    COLLEGE,
    GREY_SHIRT,
    HS,
    LEFT,
    RED_SHIRT,
    RED_SHIRT_PLUS_WAIVER,
)
from player_tracking.models import AnnualRoster, Player, Transaction

FIRST_NEW_RULES_HS_GRAD_YEAR = 2026
FIRST_TRANSITION_HS_GRAD_YEAR = 2022
LAST_TRANSITION_HS_GRAD_YEAR = 2025
LAST_OLD_RULES_SPRING = 2026


def set_player_props_get_errors():
    calc_first_spring()
    errors = calc_last_spring()
    return errors


def calc_first_spring():
    players = Player.objects.all()
    for player in players:
        this_player = Player.objects.get(pk=player.pk)
        players_transactions = Transaction.objects.filter(player=player).order_by(
            "trans_date"
        )
        for trans in players_transactions:
            if trans.trans_event in HS:
                this_player.first_spring = this_player.hsgrad_year + 1
                this_player.save()
                break
            if trans.trans_event in COLLEGE:
                if trans.trans_date.month > 8:
                    this_player.first_spring = trans.trans_date.year + 2
                else:
                    this_player.first_spring = trans.trans_date.year + 1
                this_player.save()
                break


def calc_last_spring():
    players = Player.objects.all()
    errors = []
    for player in players:
        this_player = Player.objects.get(pk=player.pk)
        players_transactions = Transaction.objects.filter(player=player).order_by(
            "-trans_date"
        )
        last_effective_transaction = determine_last_effective_transaction(
            players_transactions
        )
        if not last_effective_transaction:
            errors.append(f"missing transaction for {player.first} {player.last}")
            continue
        if last_effective_transaction.trans_event in LEFT:
            set_leaving_player(this_player, last_effective_transaction)
            continue
        if this_player.hsgrad_year >= FIRST_NEW_RULES_HS_GRAD_YEAR:
            eligibility_start_spring = get_eligibility_start_spring(player)
            if eligibility_start_spring is not None:
                this_player.last_spring = eligibility_start_spring + 4
                this_player.save()
                continue
        rosters = AnnualRoster.objects.filter(player=player).order_by("spring_year")
        if not rosters:
            old_last_spring = player.hsgrad_year + 4
            this_player.last_spring = transition_last_spring(
                player, old_last_spring
            )
            this_player.save()
            continue
        total_years = calc_total_years_eligible(errors, player, rosters)
        old_last_spring = player.hsgrad_year + total_years
        this_player.last_spring = transition_last_spring(player, old_last_spring)
        this_player.save()
    return errors


def transition_last_spring(player, old_last_spring):
    in_transition_cohort = (
        FIRST_TRANSITION_HS_GRAD_YEAR
        <= player.hsgrad_year
        <= LAST_TRANSITION_HS_GRAD_YEAR
    )
    old_eligibility_remains = old_last_spring > LAST_OLD_RULES_SPRING
    eligibility_start_spring = get_eligibility_start_spring(player)
    if (
        in_transition_cohort
        and old_eligibility_remains
        and eligibility_start_spring is not None
    ):
        new_last_spring = eligibility_start_spring + 4
        return max(old_last_spring, new_last_spring)
    return old_last_spring


def get_eligibility_start_spring(player) -> int:
    first_roster_year = (
        AnnualRoster.objects.filter(player=player)
        .order_by("spring_year")
        .values_list("spring_year", flat=True)
        .first()
    )
    if first_roster_year is not None:
        return first_roster_year
    return player.hsgrad_year + 1


def determine_last_effective_transaction(players_transactions):
    last_effective_transaction = None
    for transaction in players_transactions:
        if transaction.trans_event in AFTER:
            continue
        else:
            last_effective_transaction = transaction
            break
    return last_effective_transaction


def set_leaving_player(this_player, last_effective_transaction):
    last_spring = last_effective_transaction.trans_date.year
    if last_effective_transaction.trans_date.month > 8:
        last_spring = last_effective_transaction.trans_date.year + 1
    this_player.last_spring = last_spring
    if this_player.hsgrad_year >= last_spring:
        this_player.first_spring = None
        this_player.last_spring = None
    this_player.via_exhaust = False
    this_player.save()


def calc_total_years_eligible(errors, player, rosters):
    red_shirt_used = False
    clock_started = False
    total_years = 4
    roster_year = player.hsgrad_year + 1
    for roster in rosters:
        redshirt_clock = False
        if roster.status in RED_SHIRT or roster.status in GREY_SHIRT:
            redshirt_clock = True
        if roster_year != roster.spring_year:
            errors.append(
                f"missing roster year {roster_year} for {player.first} {player.last}"
            )
        if not clock_started and roster.status in GREY_SHIRT:
            total_years += 1
        elif redshirt_clock and not red_shirt_used or roster.status in RED_SHIRT_PLUS_WAIVER:
            total_years += 1
            red_shirt_used = True
        roster_year += 1
        clock_started = True
    return total_years
