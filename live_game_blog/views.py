from django.shortcuts import render

def games(request):
    return render(request, "live_game_blog/games.html")
