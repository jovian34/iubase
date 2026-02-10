from django import urls

from conference.views import conf_year, add_series, conf_schedule, add_win, standings, conf_index, pickem_index, pickem_register, my_pickem, choose_pick


urlpatterns = [
    urls.path("index/", conf_index.view, name="conf_index"),
    urls.path("members/<conf>/<spring_year>/", conf_year.view, name="conf_year"),
    urls.path("members/<conf>/", conf_year.view, name="conf_year_default"),
    urls.path("add_series/<spring_year>/", add_series.view, name="add_series"),
    urls.path("add_series/", add_series.view, name="add_series_default"),
    urls.path("schedule/<spring_year>/", conf_schedule.view, name="conf_schedule"),
    urls.path(
        "schedule/<spring_year>/<month>/<day>/",
        conf_schedule.week,
        name="conf_schedule_week",
    ),
    urls.path("pickem_index/<spring_year>/", pickem_index.view, name="pickem_index"),
    urls.path("pickem_register/<spring_year>/", pickem_register.view, name="pickem_register"),
    urls.path("my_pickem/<spring_year>/", my_pickem.view, name="my_pickem"),
    urls.path("choose_pick/<series>/<pick>/", choose_pick.view, name="choose_pick"),
    urls.path("add_away_win/<conf_series>/", add_win.away, name="add_away_win"),
    urls.path("add_home_win/<conf_series>/", add_win.home, name="add_home_win"),
    urls.path("add_tie/<conf_series>/", add_win.tie, name="add_tie"),
    urls.path(
        "standings/<spring_year>/",
        standings.view,
        name="standings",
    ),
]
