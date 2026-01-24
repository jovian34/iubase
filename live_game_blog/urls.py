from django.urls import path
from live_game_blog.views import (
    games,
    add_blog_entry_only,
    add_blog_plus_scoreboard,
    add_home_stadium_data,
    add_team,
    add_game,
    edit_blog_entry,
    edit_game_info,
    live_game_blog,
    schedule,
    stadiums,
)


urlpatterns = [
    path("", games.upcoming, name="games"),
    path("games/", games.upcoming, name="games"),
    path("schedule/<spring_year>/", schedule.view, name="schedule"),
    path("schedule/", schedule.view, name="schedule"),
    path("live_game_blog/<game_pk>/", live_game_blog.view, name="live_game_blog"),
    path("add_game/", add_game.view, name="add_game"),
    path("add_team/", add_team.view, name="add_team"),
    path("stadiums/", stadiums.view, name="stadiums"),
    path(
        "add_home_stadium_data/<team_pk>/",
        add_home_stadium_data.view,
        name="add_home_stadium_data",
    ),
    # partials
    path("past_games/", games.past, name="past_games"),
    path(
        "add_blog_entry_only/<game_pk>/",
        add_blog_entry_only.view,
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
    path("add_neutral_game/", add_game.neutral, name="add_neutral_game"),
    path("edit_game_info/<game_pk>", edit_game_info.view, name="edit_game_info"),
    path(
        "teams_wo_stad_config/",
        stadiums.teams_wo_stad_config,
        name="teams_wo_stad_config",
    ),
]
