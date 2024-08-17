from player_tracking.models import AnnualRoster, Player, SummerAssign, Transaction
from player_tracking.choices import AFTER, GREY_SHIRT, RED_SHIRT, RED_SHIRT_PLUS_WAIVER, HS, COLLEGE, LEFT


def save_new_player_and_init_transaction(form):
    add_player = Player.objects.create(
                first=form.cleaned_data["first"],
                last=form.cleaned_data["last"],
                hsgrad_year=form.cleaned_data["hsgrad_year"],
                high_school=form.cleaned_data["high_school"],
                home_city=form.cleaned_data["home_city"],
                home_state=form.cleaned_data["home_state"],
                home_country=form.cleaned_data["home_country"],
                headshot=form.cleaned_data["headshot"],
                birthdate=form.cleaned_data["birthdate"],
                bats=form.cleaned_data["bats"],
                throws=form.cleaned_data["throws"],
                height=form.cleaned_data["height"],
                weight=form.cleaned_data["weight"],
            )
    add_player.save()
    this_player = Player.objects.last()
    add_initial_transaction = Transaction(
                player=this_player,
                trans_event=form.cleaned_data["trans_event"],
                trans_date=form.cleaned_data["trans_date"],
                citation=form.cleaned_data["citation"],
                primary_position=form.cleaned_data["primary_position"],
            )
    add_initial_transaction.save()


def save_transaction_form(player_id, form):
    add_transaction = Transaction.objects.create(
                player=Player.objects.get(pk=player_id),
                trans_event=form.cleaned_data["trans_event"],
                trans_date=form.cleaned_data["trans_date"],
                citation=form.cleaned_data["citation"],
                primary_position=form.cleaned_data["primary_position"],
                other_team=form.cleaned_data["other_team"],
                prof_org=form.cleaned_data["prof_org"],
                draft_round=form.cleaned_data["draft_round"],
                bonus_or_slot=form.cleaned_data["bonus_or_slot"],
                comment=form.cleaned_data["comment"],
            )
    add_transaction.save()


def save_roster_year(player_id, form):
    add_roster = AnnualRoster.objects.create(
                spring_year=form.cleaned_data["spring_year"],
                team=form.cleaned_data["team"],
                player=Player.objects.get(pk=player_id),
                jersey=form.cleaned_data["jersey"],
                status=form.cleaned_data["status"],
                primary_position=form.cleaned_data["primary_position"],
                secondary_position=form.cleaned_data["secondary_position"],
            )
    add_roster.save()

def save_summer_assign(player_id, form):
    add_assign = SummerAssign.objects.create(
                player=Player.objects.get(pk=player_id),
                summer_year=form.cleaned_data["summer_year"],
                summer_league=form.cleaned_data["summer_league"],
                summer_team=form.cleaned_data["summer_team"],
                source=form.cleaned_data["source"],
                citation=form.cleaned_data["citation"],
            )
    add_assign.save()


def set_leaving_player(this_player, last_effective_transaction):
    this_player.last_spring = last_effective_transaction.trans_date.year
    if this_player.hsgrad_year == last_effective_transaction.trans_date.year:
        this_player.first_spring = None
        this_player.last_spring = None
    this_player.save()


def determine_last_effective_transaction(players_transactions):
    last_effective_transaction = None
    for transaction in players_transactions:
        if transaction.trans_event in AFTER:
            continue
        else:
            last_effective_transaction = transaction
            break
    return last_effective_transaction


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


def calc_first_spring():
    players = Player.objects.all()
    for player in players:
        this_player = Player.objects.get(pk=player.pk)
        players_transactions = Transaction.objects.filter(player=player).order_by("trans_date")
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
        players_transactions = Transaction.objects.filter(player=player).order_by("-trans_date")
        last_effective_transaction = determine_last_effective_transaction(players_transactions)
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
            

def set_player_props_get_errors():
    calc_first_spring()
    errors = calc_last_spring()
    return errors