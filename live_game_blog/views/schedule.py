import datetime
import pytz

from django import shortcuts
from live_game_blog import models as lgb_models

from django.db.models import Q


eastern = pytz.timezone("America/New_York")
spring_year = datetime.date.today().year
if datetime.date.today().month > 8:
    spring_year = datetime.date.today().year + 1


def view(request, spring_year=spring_year):
    template_path = "live_game_blog/schedule.html"
    iu = lgb_models.Team.objects.get(team_name="Indiana")
    context = {
        "games": lgb_models.Game.objects.filter(
            Q(
                first_pitch__gt=eastern.localize(
                    datetime.datetime(int(spring_year), 2, 1)
                )
            )
            & Q(
                first_pitch__lt=eastern.localize(
                    datetime.datetime(int(spring_year), 8, 1)
                )
            )
            & (Q(home_team=iu) | Q(away_team=iu))
        ).order_by("first_pitch"),
        "page_title": f"{spring_year} Indiana University Baseball Schedule",
        "spring_year": int(spring_year),
    }
    return shortcuts.render(request, template_path, context)
