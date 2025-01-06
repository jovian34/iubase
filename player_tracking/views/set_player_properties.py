from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from player_tracking.models import AnnualRoster, Player, Transaction
from player_tracking.choices import (
    AFTER,
    GREY_SHIRT,
    RED_SHIRT,
    RED_SHIRT_PLUS_WAIVER,
    HS,
    COLLEGE,
    LEFT,
)


@login_required
def view(request):
    errors = set_player_props_get_errors()
    players_updated = Player.objects.all().order_by("last")
    context = {
        "players": players_updated,
        "error_exists": bool(len(errors)),
        "errors": errors,
        "page_title": "Errors From Last Spring Calculations",
    }
    return render(request, "player_tracking/calc_last_spring.html", context)


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
        rosters = AnnualRoster.objects.filter(player=player).order_by("spring_year")
        if not rosters:
            this_player.last_spring = player.hsgrad_year + 4
            this_player.save()
            continue
        total_years = calc_total_years_eligible(errors, player, rosters)
        this_player.last_spring = player.hsgrad_year + total_years
        this_player.save()
    return errors


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
    this_player.last_spring = last_effective_transaction.trans_date.year
    if this_player.hsgrad_year == last_effective_transaction.trans_date.year:
        this_player.first_spring = None
        this_player.last_spring = None
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
        elif redshirt_clock and not red_shirt_used:
            total_years += 1
            red_shirt_used = True
        elif roster.status in RED_SHIRT_PLUS_WAIVER:
            total_years += 1
            red_shirt_used = True
        roster_year += 1
        clock_started = True
    return total_years
