from django import urls

from conference.views import conf_year, add_series


urlpatterns = [
    urls.path("members/<conf>/<spring_year>/", conf_year.view, name="conf_year"),
    urls.path("members/<conf>/", conf_year.view, name="conf_year_default"),
    urls.path("add_series/<spring_year>/", add_series.view, name="add_series"),
    urls.path("add_series/", add_series.view, name="add_series_default"),
]