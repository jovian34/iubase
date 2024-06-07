from django.urls import path
from player_tracking import views

urlpatterns = [
    path("", views.pt_index, name="pt_index"),
    path("players/", views.players, name="players"),
    path("player_rosters/<player_id>/", views.player_rosters, name="player_rosters"),  
    path("spring_depth_chart/<spring_year>/", views.spring_depth_chart, name="spring_depth_chart"),
    path("fall_depth_chart/<fall_year>/", views.fall_depth_chart, name="fall_depth_chart"),
    path("fall_roster/<fall_year>/", views.fall_roster, name="fall_roster"),
    path("spring_roster/<spring_year>/", views.spring_roster, name="spring_roster"),
    path("add_player/", views.add_player, name="add_player"),
    path("portal/<portal_year>/", views.portal, name="portal"),
    path("calc_last_spring/", views.calc_last_spring, name="calc_last_spring"),
    path("projected_players_fall/<fall_year>/", views.projected_players_fall, name="projected_players_fall"),

    # partials
    path("add_roster_year/<player_id>/", views.add_roster_year, name="add_roster_year"),
    path("add_transaction/<player_id>/", views.add_transaction, name="add_transaction"),
]
