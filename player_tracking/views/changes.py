from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from player_tracking.models import (
    Player,
    Transaction,
    AnnualRoster,
    SummerAssign,
)
from live_game_blog.models import Team
from player_tracking.forms import AnnualRosterForm, NewPlayerForm, TransactionForm, SummerAssignForm
from player_tracking.choices import (
    LEFT,
    AFTER,
    GREY_SHIRT,
    RED_SHIRT,
    RED_SHIRT_PLUS_WAIVER,
    COLLEGE,
    HS,
)
from player_tracking.views.changes_logic import save_transaction_form


@login_required
def add_player(request):
    if request.method == "POST":
        form = NewPlayerForm(request.POST)
        if form.is_valid():
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
        return redirect(reverse("players"))
    else:
        form = NewPlayerForm(
            initial={
                "hsgrad_year": timezone.now().year,
                "home_country": "USA",
            },
        )
        context = {
            "form": form,
            "page_title": "Add a New Player",
        }
        return render(request, "player_tracking/add_player.html", context)


@login_required
def add_roster_year(request, player_id):
    if request.method == "POST":
        form = AnnualRosterForm(request.POST)
        if form.is_valid():
            add_roster = AnnualRoster.objects.create(
                spring_year=form.cleaned_data["spring_year"],
                team=form.cleaned_data["team"],
                player=Player.objects.get(pk=player_id),
                jersey=form.cleaned_data["jersey"],
                status=form.cleaned_data["status"],
                primary_position=form.cleaned_data["primary_position"],
                secondary_position=form.cleaned_data["secondary_position"],
            )
            # process to increase clock
            add_roster.save()
        else:
            print("FORM IS NOT VALID")

        return redirect(reverse("player_rosters", args=[player_id]))
    else:
        form = AnnualRosterForm(
            initial={
                "spring_year": timezone.now().year,
                "team": Team.objects.get(team_name="Indiana"),
            },
        )
        context = {
            "form": form,
            "player_id": player_id,
        }
        return render(
            request,
            "player_tracking/partials/add_roster_year.html",
            context,
        )


@login_required
def add_summer_assignment(request, player_id):
    if request.method== "POST":
        form = SummerAssignForm(request.POST)
        if form.is_valid():
            add_assign = SummerAssign.objects.create(
                player=Player.objects.get(pk=player_id),
                summer_year=form.cleaned_data["summer_year"],
                summer_league=form.cleaned_data["summer_league"],
                summer_team=form.cleaned_data["summer_team"],
                source=form.cleaned_data["source"],
                citation=form.cleaned_data["citation"],
            )
            add_assign.save()
        return redirect(reverse("player_rosters", args=[player_id]))
    else:
        form = SummerAssignForm(
            initial={
                "summer_year": timezone.now().year,
            },
        )
        context = {
            "player_id": player_id,
            "form": form,
        }
        return render(
            request,
            "player_tracking/partials/add_summer_assignment.html",
            context,
        )
    
@login_required
def add_transaction(request, player_id):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            save_transaction_form(player_id, form)
        return redirect(reverse("player_rosters", args=[player_id]))
    else:
        form = TransactionForm(
            initial={
                "trans_date": timezone.now().year,
            },
        )
        context = {
            "form": form,
            "player_id": player_id,
        }
        return render(
            request,
            "player_tracking/partials/add_transaction.html",
            context,
        )


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
                this_player.first_spring = trans.trans_date.year + 1
                this_player.save()
                break

@login_required
def calc_last_spring(request):
    calc_first_spring()
    players = Player.objects.all()
    errors = []
    for player in players:
        this_player = Player.objects.get(pk=player.pk)
        players_transactions = Transaction.objects.filter(player=player).order_by("-trans_date")
        last_transaction = None
        for transaction in players_transactions:
            if transaction.trans_event in AFTER:
                continue
            else:
                last_transaction = transaction
                break
        if not last_transaction:
            errors.append(f"missing transaction for {player.first} {player.last}")
        if last_transaction.trans_event in LEFT:
            this_player.last_spring = last_transaction.trans_date.year
            if this_player.hsgrad_year == last_transaction.trans_date.year:
                this_player.first_spring = None
                this_player.last_spring = None
            this_player.save()
            continue
        red_shirt_used = False
        clock_started = False
        rosters = AnnualRoster.objects.filter(player=player).order_by("spring_year")
        if not rosters:
            this_player.last_spring = player.hsgrad_year + 4
            this_player.save()
            continue
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
        this_player.last_spring = player.hsgrad_year + total_years
        this_player.save()
    players_updated = Player.objects.all().order_by("last")
    context = {
        "players": players_updated,
        "error_exists": bool(len(errors)),
        "errors": errors,
        "page_title": "Errors From Last Spring Calculations",
    }
    return render(request, "player_tracking/calc_last_spring.html", context)

