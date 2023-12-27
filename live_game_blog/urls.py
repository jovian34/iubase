from django.urls import path
from . import views

urlpatterns = [
    path("", views.games, name="games"),
    path("games/", views.games, name="games"),
    # partials
    path("team_logo/<team_pk>/", views.team_logo, name="team_logo"),
    path("past_games/", views.past_games, name="past_games"),
    path("live_game_blog/<game_pk>/", views.live_game_blog, name="live_game_blog")
]
