from django.urls import path
from player_tracking.views import (
    add_player,
    add_roster_year,
    add_summer_assignment,
    add_transaction,
    all_players,
    depth_charts, 
    draft_combine, 
    drafted_players, 
    fall_players, 
    iu_rosters,
    pt_index, 
    set_player_properties,
    single_player_page, 
    summer_assignments, 
    transfer_portal
)


urlpatterns = [
    path("", pt_index.view, name="pt_index"),
    path("players/", all_players.view, name="players"),
    path("player/<player_id>/", single_player_page.view, name="single_player_page"),
    path(
        "spring_depth_chart/<spring_year>/",
        depth_charts.spring_depth_chart,
        name="spring_depth_chart",
    ),
    path(
        "fall_depth_chart/<fall_year>/",
        depth_charts.fall_depth_chart,
        name="fall_depth_chart",
    ),
    path("spring_roster/<spring_year>/", iu_rosters.spring, name="spring_roster"),
    path("add_player/", add_player.view, name="add_player"),
    path("portal/<portal_year>/", transfer_portal.view, name="portal"),
    path(
        "set_player_properties/",
        set_player_properties.view,
        name="set_player_properties",
    ),
    path(
        "draft_combine_attendees/<draft_year>/",
        draft_combine.view,
        name="draft_combine_attendees",
    ),
    path(
        "drafted_players/<draft_year>/",
        drafted_players.view,
        name="drafted_players",
    ),
    path(
        "fall_players/",
        fall_players.fall_players,
        name="fall_players",
    ),
    path(
        "fall_players/<fall_year>/",
        fall_players.fall_players,
        name="fall_players",
    ),
    path(
        "projected_players_fall/<fall_year>/",
        fall_players.projected,
        name="projected_players_fall",
    ),
    path(
        "all_eligible_players_fall/<fall_year>/",
        fall_players.all_eligible,
        name="all_eligible_players_fall",
    ),
    path(
        "summer_assignments/<summer_year>/",
        summer_assignments.view,
        name="summer_assignments",
    ),
    
    # partials
    path(
        "add_roster_year/<player_id>/", add_roster_year.view, name="add_roster_year"
    ),
    path(
        "add_transaction/<player_id>/", add_transaction.view, name="add_transaction"
    ),
    path(
        "add_summer_assignment/<player_id>/",
        add_summer_assignment.view,
        name="add_summer_assignment",
    ),
    path(
        "fall_players_redirect/",
        fall_players.fall_players_redirect,
        name="fall_players_redirect",
    ),
    path("fall_roster/<fall_year>/", iu_rosters.fall, name="fall_roster"),
]
