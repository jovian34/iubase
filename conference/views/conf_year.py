import datetime

from django import shortcuts
from django.db.models import Q

from conference import models as conf_models


spring_year = datetime.date.today().year
if datetime.date.today().month > 8:
    spring_year = spring_year + 1


def view(request, conf, spring_year=spring_year):
    conference = conf_models.Conference.objects.get(abbrev=conf)
    all_conf_teams = conf_models.ConfTeam.objects.filter(conference=conference)
    this_conf_teams = get_conf_teams_for_requested_year(spring_year, conference, all_conf_teams)
    context = {
        "teams": this_conf_teams,
        "conference": conference,
        "spring_year": spring_year,
        "page_title": f"{conference.long_name} members for {spring_year}"
    }

    return shortcuts.render(request, "conference/conf_year.html", context)


def get_conf_teams_for_requested_year(spring_year, conference, all_conf_teams):
    all_team = []
    for conf_team in all_conf_teams:
        all_team.append(conf_team.team)
    all_team = set(all_team)
    this_conf_teams = []
    for team in all_team:
        conf_joins = conf_models.ConfTeam.objects.filter(
            Q(team=team),
            Q(fall_year_joined__lt=int(spring_year)),
        ).order_by("-fall_year_joined")
        try:
            if conf_joins[0].conference == conference:
                this_conf_teams.append(conf_joins[0].team)
        except IndexError:
            pass
    return sorted(this_conf_teams, key=lambda team: team.team_name)