from django import urls

from conference.views import conf_year


urlpatterns = [
    urls.path("<conf>/<spring_year>/", conf_year.view, name="conf_year"),
]