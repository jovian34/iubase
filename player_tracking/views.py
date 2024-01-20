from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from player_tracking.models import Player, Transaction, AnnualRoster
from live_game_blog.models import Team
from player_tracking.forms import AnnualRosterForm, NewPlayerForm
from player_tracking.choices import POSITION_CHOICES


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
                clock=form.cleaned_data["clock"],                
            )
            add_player.save()
        return redirect(reverse("players"))
    else:
        form = NewPlayerForm(
            initial={
                "hsgrad_year": timezone.now().year,
                "home_country": "USA",
                "clock": 5,
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
    context = {
        "player": player,
        "page_title": f"{player.first} {player.last} rosters",
        "rosters": rosters,
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
            add_roster.save()
        else:
            print("FORM IS NOT VALID")

        return redirect(reverse("player_rosters", args=[player_id]))
    else:
        player = Player.objects.get(pk=player_id)
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
    players = AnnualRoster.objects.filter(spring_year=spring_year).filter(team__team_name="Indiana").filter(status="Spring Roster").order_by("jersey")
    if players:
        page_title = f"Spring {spring_year} Roster"
    else:
        page_title = f"Spring {spring_year} Roster not yet announced"
    context = {
        "players": players,
        "page_title": page_title,
        "total": len(players),
    }
    return render(request, "player_tracking/roster.html", context)