from django.shortcuts import render

def players(request):
    return render(request, "player_tracking/players.html")
