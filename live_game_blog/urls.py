from django.urls import path
from live_game_blog import views

urlpatterns = [
    path("", views.games, name="games"),
    path("games/", views.games, name="games"),
    path("live_game_blog/<game_pk>/", views.live_game_blog, name="live_game_blog"),
    path(
        "edit_live_game_blog/<game_pk>/",
        views.edit_live_game_blog,
        name="edit_live_game_blog",
    ),
    path("add_game", views.add_game, name="add_game"),
    path("add_team", views.add_team, name="add_team"),
    # partials
    path("past_games/", views.past_games, name="past_games"),
    path(
        "add_blog_entry_only/<game_pk>/",
        views.add_blog_entry_only,
        name="add_blog_entry_only",
    ),
    path(
        "add_blog_plus_scoreboard/<game_pk>/",
        views.add_blog_plus_scoreboard,
        name="add_blog_plus_scoreboard",
    ),
    path(
        "edit_blog_entry/<entry_pk>/",
        views.edit_blog_entry,
        name="edit_blog_entry",
    ),
]
