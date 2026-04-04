from django import shortcuts

from conference import models as conf_models
from conference.logic import year
from conference.views import conf_year
from conference.logic import crpi

spring_year = year.get_spring_year()


def view(request, spring_year=spring_year):
    conference = conf_models.Conference.objects.get(abbrev="B1G")
    all_conf_teams = conf_models.ConfTeam.objects.filter(conference=conference)
    this_conf_teams = conf_year.get_conf_teams_for_requested_year(
        spring_year, conference, all_conf_teams
    )

    crpi_rows = crpi.build_crpi_rows(this_conf_teams, int(spring_year))

    context = {
        "page_title": f"{spring_year} B1G cRPI",
        "crpi_rows": crpi_rows,
        "spring_year": spring_year,
    }
    return shortcuts.render(request, "conference/crpi.html", context)