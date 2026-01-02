from django import urls

from conference.views import conf_year, add_series, conf_schedule, add_win


urlpatterns = [
    urls.path("members/<conf>/<spring_year>/", conf_year.view, name="conf_year"),
    urls.path("members/<conf>/", conf_year.view, name="conf_year_default"),
    urls.path("add_series/<spring_year>/", add_series.view, name="add_series"),
    urls.path("add_series/", add_series.view, name="add_series_default"),
    urls.path("conf_schedule/<spring_year>/", conf_schedule.view, name="conf_schedule"),
    urls.path("conf_schedule/<spring_year>/<month>/<day>/", conf_schedule.week, name="conf_schedule_week"),
    urls.path("add_away_win/<conf_series>/", add_win.away, name="add_away_win"),
    urls.path("add_home_win/<conf_series>/", add_win.home, name="add_home_win"),
    urls.path("add_tie/<conf_series>/", add_win.tie, name="add_tie"),
]