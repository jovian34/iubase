from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from datetime import date, datetime

from player_tracking.models import (
    Player,
    Transaction,
    AnnualRoster,
    MLBDraftDate,
    SummerAssign,
    SummerLeague,
    SummerTeam,
)
from live_game_blog.models import Team
from index.views import save_traffic_data
from player_tracking.forms import AnnualRosterForm, NewPlayerForm, TransactionForm, SummerAssignForm
from player_tracking.choices import (
    POSITION_CHOICES,
    LEFT,
    JOINED,
    AFTER,
    ROSTERED,
    GREY_SHIRT,
    RED_SHIRT,
    RED_SHIRT_PLUS_WAIVER,
)


def players(request):
    players = Player.objects.all().order_by("last")
    context = {
        "players": players,
        "page_title": "Players",
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/players.html", context)


def pt_index(request):
    today = timezone.now().date()
    if today.month < 8:
        current_spring = today.year
        current_fall = current_spring - 1
    else:
        current_fall = today.year
        current_spring = current_fall + 1
    context = {
        "fall": current_fall,
        "spring": current_spring,
        "page_title": "Player Tracking",
        "this_year": str(today.year),
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/pt_index.html", context)


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


def player_rosters(request, player_id):
    player = Player.objects.get(pk=player_id)
    rosters = AnnualRoster.objects.filter(player=player).order_by("-spring_year")
    transactions = Transaction.objects.filter(player=player).order_by("-trans_date")
    summers = SummerAssign.objects.filter(player=player).order_by("-summer_year")
    context = {
        "player": player,
        "page_title": f"{player.first} {player.last}",
        "rosters": rosters,
        "transactions": transactions,
        "summers": summers,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/player_rosters.html", context)


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
            add_transaction = Transaction.objects.create(
                player=Player.objects.get(pk=player_id),
                trans_event=form.cleaned_data["trans_event"],
                trans_date=form.cleaned_data["trans_date"],
                citation=form.cleaned_data["citation"],
                primary_position=form.cleaned_data["primary_position"],
            )
            add_transaction.save()
        else:
            print("FORM IS NOT VALID")
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


def fall_depth_chart(request, fall_year):
    spring_year = int(fall_year) + 1
    fall_statuses = ["Fall Roster", "Spring Roster"]
    positions = [position[0] for position in POSITION_CHOICES]
    players = (
        AnnualRoster.objects.filter(spring_year=spring_year)
        .filter(team__team_name="Indiana")
        .filter(status__in=fall_statuses)
        .order_by("player__last")
    )
    context = {
        "players": players,
        "page_title": f"Fall {fall_year} Available Depth Chart",
        "positions": positions,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/depth_chart.html", context)


def spring_depth_chart(request, spring_year):
    positions = [position[0] for position in POSITION_CHOICES]
    players = (
        AnnualRoster.objects.filter(spring_year=spring_year)
        .filter(team__team_name="Indiana")
        .filter(status="Spring Roster")
        .order_by("player__last")
    )
    if players:
        page_title = f"Spring {spring_year} Available Depth Chart"
    else:
        page_title = f"Spring {spring_year} Roster not yet announced"
    context = {
        "players": players,
        "page_title": page_title,
        "positions": positions,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/depth_chart.html", context)


def fall_roster(request, fall_year):
    spring_year = int(fall_year) + 1
    players = (
        AnnualRoster.objects.filter(spring_year=spring_year)
        .filter(team__team_name="Indiana")
        .order_by("jersey")
    )
    context = {
        "players": players,
        "page_title": f"Fall {fall_year} Roster",
        "total": len(players),
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/roster.html", context)


def spring_roster(request, spring_year):
    all_roster = [
        "Spring Roster",
        "On Spring Roster but did not play",
        "Played but granted eligibility waiver",
    ]
    players = (
        AnnualRoster.objects.filter(spring_year=spring_year)
        .filter(team__team_name="Indiana")
        .filter(status__in=all_roster)
        .order_by("jersey")
    )
    if len(players) < 5 and int(spring_year) >= timezone.now().date().year:
        page_title = f"Spring {spring_year} Roster not fully announced"
    else:
        page_title = f"Spring {spring_year} Roster"
    context = {
        "players": players,
        "page_title": page_title,
        "total": len(players),
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/roster.html", context)


def portal(request, portal_year):
    outgoing = Transaction.objects.filter(
        trans_event="Entered Transfer Portal",
        trans_date__year=portal_year,
    ).order_by("player__last")
    incoming = Transaction.objects.filter(
        trans_event="Verbal Commitment from College",
        trans_date__year=portal_year,
    ).order_by("player__last")
    context = {
        "outgoing": outgoing,
        "incoming": incoming,
        "page_title": f"{portal_year} Transfer Portal",
        "total_out": str(len(outgoing)),
        "total_in": str(len(incoming)),
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/portal.html", context)


def calc_first_spring():
    players = Player.objects.all()
    for player in players:
        this_player = Player.objects.get(pk=player.pk)
        players_transactions = Transaction.objects.filter(player=player).order_by("trans_date")
        for trans in players_transactions:
            hs = [
                "Verbal Commitment from High School",
                "National Letter of Intent Signed",
            ]
            college = [
                "Verbal Commitment from College",
            ]
            if trans.trans_event in hs:
                this_player.first_spring = this_player.hsgrad_year + 1
                this_player.save()
                break
            if trans.trans_event in college:
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


def sort_by_positions(players):
    lhp = {"position": "Left Handed Pitcher", "players": [],}
    rhp = {"position": "Right Handed Pitcher", "players": [],}
    catcher = {"position": "Catcher", "players": [],}
    infielder = {"position": "Infielder", "players": [],}
    outfielder = {"position": "Outfielder", "players": [],}
    dh = {"position": "Designated Hitter", "players": [],}
    for player in players:
        if player.throws == "Left" and player.position == "Pitcher":
            lhp["players"].append(player)
        elif player.throws == "Right" and player.position == "Pitcher":
            rhp["players"].append(player)
        elif player.position == "Catcher":
            catcher["players"].append(player)
        elif player.position in ["First Base", "Second Base", "Third Base", "Shortstop"]:
            infielder["players"].append(player)
        elif player.position in ["Centerfield", "Corner Outfield"]:
            outfielder["players"].append(player)
        else:
            dh["players"].append(player)
    positions = [lhp, rhp, catcher, infielder, outfielder, dh]
    for position in positions:
        position["count"] = len(position["players"])
    return positions


def projected_players_fall(request, fall_year):
    try:
        draft_date = MLBDraftDate.objects.get(fall_year=fall_year)
    except MLBDraftDate.DoesNotExist:
        return redirect("pt_index")
    
    players = Player.objects.filter(last_spring__gte=(int(fall_year) + 1)).order_by(
        "last"
    )

    draft_pending = True
    if draft_date.latest_draft_day < datetime.now().date():
        draft_pending = False
    if draft_date.draft_complete:
        draft_pending = False
    for player in players:
        roster_draft = AnnualRoster.objects.filter(player=player)
        if len(roster_draft) > 2 and draft_pending:
            player.draft = f"*{fall_year} MLB Draft Eligible"
        roster = AnnualRoster.objects.filter(
            player=player, spring_year=fall_year
        ).first()
        if roster:
            if player.birthdate:
                if player.birthdate <= draft_date.latest_birthdate and draft_pending:
                    player.draft = f"*{fall_year} MLB Draft Eligible"
            player.position = roster.primary_position
            if roster.team.mascot == "Hoosiers":
                player.group = "Returning"
            else:
                player.group = "Transfer"
        else:
            player.group = "Freshman"
            if draft_pending:
                player.draft = f"*{fall_year} MLB Draft Eligible from High School"
            sep1 = date(int(fall_year), 9, 1)
            transactions = Transaction.objects.filter(
                player=player, trans_date__lte=sep1
            ).order_by("-trans_date")
            for transaction in transactions:
                if transaction.primary_position:
                    player.position = transaction.primary_position
                    break
                else:
                    player.position = None
    count = len(players)
    positions = sort_by_positions(players)
    context = {
        "players": players,
        "page_title": f"Projected Players For Fall {fall_year}",
        "count": count,
        "positions": positions,    
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/projected_players_fall.html", context)


def draft_combine_attendees(request, this_year):
    draft_date = MLBDraftDate.objects.get(fall_year=int(this_year))
    draft_date = draft_date.latest_draft_day

    count = 0
    players = Player.objects.all().order_by("last")
    for player in players:
        player.combine = False
        transactions = Transaction.objects.filter(player=player)
        for trans in transactions:
            if trans.trans_event == "Attending MLB Draft Combine" and trans.trans_date.year == int(this_year):
                player.combine = True
                player.position = trans.primary_position
                count += 1     
                if player.hsgrad_year == int(this_year):
                    player.group = "Freshman"
                else:
                    player.group = "College"

    context = {
        "this_year": this_year,
        "players": players,
        "page_title": f"All players in the {this_year} MLB Draft Combine",
        "count": count,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/draft_combine_attendees.html", context)


def summer_assignments(request, summer_year):
    assignments = SummerAssign.objects.filter(summer_year=summer_year).order_by("player__last")
    context = {
        "page_title": f"{summer_year} College Summer League Assignments for current and former Indiana players",
        "assignments": assignments,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/summer_assignments.html", context)


def drafted_players(request, draft_year):
    draft_date = MLBDraftDate.objects.get(fall_year=int(draft_year))
    draft_date = draft_date.latest_draft_day

    count = 0
    players = Player.objects.all().order_by("last")
    for player in players:
        player.drafted = False
        transactions = Transaction.objects.filter(player=player)
        for trans in transactions:
            if trans.trans_event == "Drafted" and trans.trans_date.year == int(draft_year):
                player.drafted = True
                player.position = trans.primary_position
                player.draft_round = trans.draft_round
                player.prof_org = trans.prof_org.__str__()
                count += 1     
                if player.hsgrad_year == int(draft_year):
                    player.group = "High School Signee"
                else:
                    player.group = "IU Player/Alumni"

    context = {
        "this_year": draft_year,
        "players": players,
        "page_title": f"All players selected in the {draft_year} MLB Draft",
        "count": count,
    }
    save_traffic_data(request=request, page=context["page_title"])
    return render(request, "player_tracking/drafted_players.html", context)
