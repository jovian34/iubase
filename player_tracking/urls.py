from django.urls import path
from player_tracking.views import visitor, changes, depth_charts, draft_combine, drafted_players, fall_players, iu_rosters, single_player_page, summer_assignments, transfer_portal

urlpatterns = [
    path("", visitor.pt_index, name="pt_index"),
    path("players/", visitor.players, name="players"),
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
    path("fall_roster/<fall_year>/", iu_rosters.fall, name="fall_roster"),
    path("spring_roster/<spring_year>/", iu_rosters.spring, name="spring_roster"),
    path("add_player/", changes.add_player, name="add_player"),
    path("portal/<portal_year>/", transfer_portal.view, name="portal"),
    path(
        "set_player_properties/",
        changes.set_player_properties,
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
        fall_players.fall_players_redirect,
        name="fall_players",
    ),
    path(
        "fall_players/<fall_year>/",
        fall_players.fall_players_redirect,
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
        "add_roster_year/<player_id>/", changes.add_roster_year, name="add_roster_year"
    ),
    path(
        "add_transaction/<player_id>/", changes.add_transaction, name="add_transaction"
    ),
    path(
        "add_summer_assignment/<player_id>/",
        changes.add_summer_assignment,
        name="add_summer_assignment",
    ),
]
