from decimal import Decimal
from django import shortcuts
from django.db.models import (
    Sum, F, Value, FloatField, Q, Case, When, Subquery, OuterRef,
    ExpressionWrapper, Exists, DecimalField,
)
from django.db.models.functions import Coalesce, Cast

from conference import models as conf_models
from live_game_blog import models as lgb_models


def view(request, spring_year):
    rpi_subquery = conf_models.TeamRpi.objects.filter(
        team=OuterRef('pk'),
        spring_year=spring_year
    ).values('rpi_rank')[:1]

    rpi_exists = conf_models.TeamRpi.objects.filter(
        team=OuterRef('pk'),
        spring_year=spring_year
    )

    teams_qs = lgb_models.Team.objects.annotate(
        has_rpi=Exists(rpi_exists)
    ).filter(has_rpi=True)

    teams_qs = lgb_models.Team.objects.annotate(
        has_rpi=Exists(rpi_exists)
    ).filter(has_rpi=True)

    home_wins_sq = conf_models.ConfSeries.objects.filter(
        home_team=OuterRef('pk'),
        start_date__year=spring_year
    ).values('home_team').annotate(total=Sum('home_wins')).values('total')[:1]

    away_wins_sq = conf_models.ConfSeries.objects.filter(
        away_team=OuterRef('pk'),
        start_date__year=spring_year
    ).values('away_team').annotate(total=Sum('away_wins')).values('total')[:1]

    home_losses_sq = conf_models.ConfSeries.objects.filter(
        home_team=OuterRef('pk'),
        start_date__year=spring_year
    ).values('home_team').annotate(total=Sum('away_wins')).values('total')[:1]

    away_losses_sq = conf_models.ConfSeries.objects.filter(
        away_team=OuterRef('pk'),
        start_date__year=spring_year
    ).values('away_team').annotate(total=Sum('home_wins')).values('total')[:1]

    zero_decimal = Value(Decimal('0'), output_field=DecimalField())

    teams_qs = teams_qs.annotate(
        home_wins=Coalesce(Subquery(home_wins_sq), zero_decimal),
        away_wins=Coalesce(Subquery(away_wins_sq), zero_decimal),
        home_losses=Coalesce(Subquery(home_losses_sq), zero_decimal),
        away_losses=Coalesce(Subquery(away_losses_sq), zero_decimal),
    ).annotate(
        wins=F('home_wins') + F('away_wins'),
        losses=F('home_losses') + F('away_losses'),
        rpi_rank=Subquery(rpi_subquery)
    ).annotate(
        win_pct=Case(
            When(
                Q(wins__gt=0) | Q(losses__gt=0),
                then=ExpressionWrapper(
                    Cast(F('wins'), FloatField()) / Cast(
                        (F('wins') + F('losses')), FloatField()
                    ),
                    output_field=FloatField()
                )
            ),
            default=Value(0.0),
            output_field=FloatField()
        )
    ).order_by('-win_pct',)
    
    template_path = "conference/standings.html"
    context = {
        "page_title": f"{spring_year} B1G Standings",
        "standings": teams_qs,
        "spring_year": spring_year
    }
    return shortcuts.render(request, template_path, context)