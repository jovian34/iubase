from django.urls import path
from live_game_blog.views import views, add_blog_plus_scoreboard, add_team, add_game, edit_blog_entry

urlpatterns = [
    path("", views.games, name="games"),
    path("games/", views.games, name="games"),
    path("live_game_blog/<game_pk>/", views.live_game_blog, name="live_game_blog"),
    path(
        "edit_live_game_blog/<game_pk>/",
        views.edit_live_game_blog,
        name="edit_live_game_blog",
    ),
    path("add_game", add_game.view, name="add_game"),
    path("add_team", add_team.view, name="add_team"),
    # partials
    path("past_games/", views.past_games, name="past_games"),
    path(
        "add_blog_entry_only/<game_pk>/",
        views.add_blog_entry_only,
        name="add_blog_entry_only",
    ),
    path(
        "add_blog_plus_scoreboard/<game_pk>/",
        add_blog_plus_scoreboard.view,
        name="add_blog_plus_scoreboard",
    ),
    path(
        "edit_blog_entry/<entry_pk>/",
        edit_blog_entry.view,
        name="edit_blog_entry",
    ),
]
