from django.urls import path
from . import views

urlpatterns = [
    path("", views.games, name="games"),
    path("games/", views.games, name="games"),
    path("live_game_blog/<game_pk>/", views.live_game_blog, name="live_game_blog"),
    path("edit_live_game_blog/<game_pk>/", views.edit_live_game_blog, name="edit_live_game_blog"),
    # partials
    path("past_games/", views.past_games, name="past_games"),
    path("add_blog_entry_only/<game_pk>/", views.add_blog_entry_only, name="add_blog_entry_only"),
    path("add_blog_plus_scoreboard/<game_pk>/", views.add_blog_plus_scoreboard, name="add_blog_plus_scoreboard"),
]
