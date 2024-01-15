from django.urls import path
from player_tracking import views

urlpatterns = [
    path("", views.players, name="players"),
    path("players/", views.players, name="players"),
    path("player_rosters/<player_id>/", views.player_rosters, name="player_rosters"),

    # partials
    path("add_roster_year/<player_id>/", views.add_roster_year, name="add_roster_year"),

]
