from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from datetime import date, datetime

from player_tracking.models import Player, Transaction, AnnualRoster, MLBDraftDate
from live_game_blog.models import Team
from player_tracking.forms import AnnualRosterForm, NewPlayerForm, TransactionForm
from player_tracking.choices import POSITION_CHOICES, LEFT, JOINED, ROSTERED, GREY_SHIRT, RED_SHIRT, RED_SHIRT_PLUS_WAIVER


def players(request):
    players = Player.objects.all().order_by("last")
    context = {
        "players": players,
        "page_title": "Players",
    }
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
    return render(request, "player_tracking/pt_index.html", context)


@login_required
def add_player(request):
    if request.method == "POST":
        form=NewPlayerForm(request.POST)
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
    context = {
        "player": player,
        "page_title": f"{player.first} {player.last} rosters",
        "rosters": rosters,
        "transactions": transactions,
    }
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
                secondary_position=form.cleaned_data["secondary_position"]
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
            request, "player_tracking/partials/add_roster_year.html", context,
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
            request, "player_tracking/partials/add_transaction.html", context,
        )



    

def fall_depth_chart(request, fall_year):
    spring_year = int(fall_year) + 1
    fall_statuses = ["Fall Roster", "Spring Roster"]
    positions = [ position[0] for position in POSITION_CHOICES]
    players = AnnualRoster.objects.filter(spring_year=spring_year).filter(team__team_name="Indiana").filter(status__in=fall_statuses).order_by("player__last")
    context = {
        "players": players,
        "page_title": f"Fall {fall_year} Available Depth Chart",
        "positions": positions,
    }
    return render(request, "player_tracking/depth_chart.html", context)
    

def spring_depth_chart(request, spring_year):
    positions = [ position[0] for position in POSITION_CHOICES]
    players = AnnualRoster.objects.filter(spring_year=spring_year).filter(team__team_name="Indiana").filter(status="Spring Roster").order_by("player__last")
    if players:
        page_title = f"Spring {spring_year} Available Depth Chart"
    else:
        page_title = f"Spring {spring_year} Roster not yet announced"
    context = {
        "players": players,
        "page_title": page_title,
        "positions": positions,
    }
    return render(request, "player_tracking/depth_chart.html", context)
    

def fall_roster(request, fall_year):
    spring_year = int(fall_year) + 1
    players = AnnualRoster.objects.filter(spring_year=spring_year).filter(team__team_name="Indiana").order_by("jersey")
    context = {
        "players": players,
        "page_title": f"Fall {fall_year} Roster",
        "total": len(players),
    }
    return render(request, "player_tracking/roster.html", context)
    

def spring_roster(request, spring_year):
    all_roster = ["Spring Roster", "On Spring Roster but did not play", "Played but granted eligibility waiver"]
    players = AnnualRoster.objects.filter(spring_year=spring_year).filter(team__team_name="Indiana").filter(status__in=all_roster).order_by("jersey")
    if len(players) < 5 and int(spring_year) >= timezone.now().date().year:
        page_title = f"Spring {spring_year} Roster not fully announced"
    else:
        page_title = f"Spring {spring_year} Roster"
    context = {
        "players": players,
        "page_title": page_title,
        "total": len(players),
    }
    return render(request, "player_tracking/roster.html", context)


def portal(request, portal_year):
    outgoing = Transaction.objects.filter(
        trans_event="Entered Transfer Portal",
        trans_date__year=portal_year,
    )
    incoming = Transaction.objects.filter(
        trans_event="Verbal Commitment from College",
        trans_date__year=portal_year,
    )
    context = { 
        "outgoing": outgoing,
        "incoming": incoming,
        "page_title": f"{portal_year} Transfer Portal",
        "total_out": str(len(outgoing)),
        "total_in": str(len(incoming)),
    }
    return render(request, "player_tracking/portal.html", context)


@login_required
def calc_last_spring(request):
    players = Player.objects.all()
    errors = []
    for player in players:
        this_player = Player.objects.get(pk=player.pk)
        last_transaction = Transaction.objects.filter(player=player).order_by("-trans_date").first()
        if not last_transaction:
            errors.append(f"missing transaction for {player.first} {player.last}")
        if last_transaction.trans_event in LEFT:
            this_player.last_spring = last_transaction.trans_date.year
            print(f"{this_player.last} has left the program")
            this_player.save()
            continue
        red_shirt_used = False
        clock_started = False
        rosters = AnnualRoster.objects.filter(player=player).order_by("spring_year")
        if not rosters:
            this_player.last_spring = player.hsgrad_year + 4
            print(f"{this_player.last} is incoming")
            this_player.save()
            continue
        total_years = 4
        roster_year = player.hsgrad_year + 1
        for roster in rosters:
            if roster_year != roster.spring_year:
                errors.append(f"missing roster year {roster_year} for {player.first} {player.last}")
            if not clock_started and roster.status in GREY_SHIRT:
                total_years += 1
            elif roster.status in RED_SHIRT and not red_shirt_used:
                total_years += 1
                red_shirt_used = True
            elif roster.status in RED_SHIRT_PLUS_WAIVER:
                total_years += 1
                red_shirt_used = True
            roster_year += 1
            clock_started = True
        this_player.last_spring = player.hsgrad_year + total_years
        print(f"{this_player.last} is returning")
        this_player.save()
    players_updated = Player.objects.all().order_by("last")
    context = {
        "players": players_updated,
        "errors": errors,
        "page_title": "Errors From Last Spring Calculations",
    }
    return render(request, "player_tracking/calc_last_spring.html", context)


def projected_players_fall(request, fall_year):
    players = Player.objects.filter(last_spring__gte=(int(fall_year) + 1)).order_by("last")
    
    try:
        draft_date = MLBDraftDate.objects.get(fall_year=fall_year)
    except MLBDraftDate.DoesNotExist:
        return redirect("pt_index")

    draft_pending = True
    if draft_date.latest_draft_day < datetime.now().date():
        draft_pending = False
    for player in players:
        roster_draft = AnnualRoster.objects.filter(player=player)
        if len(roster_draft) > 2 and draft_pending:
            player.draft = f"*{fall_year} MLB Draft Eligible"
        roster = AnnualRoster.objects.filter(player=player, spring_year=fall_year).first()
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
            transactions = Transaction.objects.filter(player=player, trans_date__lte=sep1).order_by("-trans_date")
            for transaction in transactions:
                if transaction.primary_position:
                    player.position = transaction.primary_position
                    continue
    count = len(players)
    context = {
        "players": players,
        "page_title": f"Projected Players For Fall {fall_year}",
        "count": count,
    }
    return render(request, "player_tracking/projected_players_fall.html", context)