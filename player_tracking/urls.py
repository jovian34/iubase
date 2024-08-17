from django.urls import path
from player_tracking.views import visitor, changes

urlpatterns = [
    path("", visitor.pt_index, name="pt_index"),
    path("players/", visitor.players, name="players"),
    path("player_rosters/<player_id>/", visitor.player_rosters, name="player_rosters"),
    path(
        "spring_depth_chart/<spring_year>/",
        visitor.spring_depth_chart,
        name="spring_depth_chart",
    ),
    path(
        "fall_depth_chart/<fall_year>/", visitor.fall_depth_chart, name="fall_depth_chart"
    ),
    path("fall_roster/<fall_year>/", visitor.fall_roster, name="fall_roster"),
    path("spring_roster/<spring_year>/", visitor.spring_roster, name="spring_roster"),
    path("add_player/", changes.add_player, name="add_player"),
    path("portal/<portal_year>/", visitor.portal, name="portal"),
    path("set_player_properties/", changes.set_player_properties, name="set_player_properties"),
    path(
        "draft_combine_attendees/<draft_year>/",
        visitor.draft_combine_attendees,
        name="draft_combine_attendees",
    ),
    path("drafted_players/<draft_year>/", visitor.drafted_players, name="drafted_players",),
    path(
        "projected_players_fall/<fall_year>/",
        visitor.projected_players_fall,
        name="projected_players_fall",
    ),
    path(
        "summer_assignments/<summer_year>/",
        visitor.summer_assignments,
        name="summer_assignments",
    ),
    # partials
    path("add_roster_year/<player_id>/", changes.add_roster_year, name="add_roster_year"),
    path("add_transaction/<player_id>/", changes.add_transaction, name="add_transaction"),
    path("add_summer_assignment/<player_id>/", changes.add_summer_assignment, name="add_summer_assignment"),
]
