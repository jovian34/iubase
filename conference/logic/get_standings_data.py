from decimal import Decimal

from django.db.models import (
    Sum, OuterRef, Subquery, Value, DecimalField, FloatField, Case, When, Q,
    F, ExpressionWrapper,
)
from django.db.models.functions import Coalesce, Cast

from conference import models as conf_models
from live_game_blog import models as lgb_models


def annotated_teams_queryset(spring_year):
    rpi_subquery = conf_models.TeamRpi.objects.filter(
        team=OuterRef('pk'),
        spring_year=spring_year
    ).values('rpi_rank')[:1]

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

    teams_qs = lgb_models.Team.objects.all()

    teams_qs = teams_qs.annotate(
        home_wins=Coalesce(Subquery(home_wins_sq), zero_decimal),
        away_wins=Coalesce(Subquery(away_wins_sq), zero_decimal),
        home_losses=Coalesce(Subquery(home_losses_sq), zero_decimal),
        away_losses=Coalesce(Subquery(away_losses_sq), zero_decimal),
        rpi_rank=Subquery(rpi_subquery),
    ).annotate(
        wins=F('home_wins') + F('away_wins'),
        losses=F('home_losses') + F('away_losses'),
    ).annotate(
        win_pct=Case(
            When(Q(wins__gt=0) | Q(losses__gt=0),
                 then=ExpressionWrapper(
                     Cast(F('wins'), FloatField()) /
                     Cast((F('wins') + F('losses')), FloatField()),
                     output_field=FloatField()
                 )
                 ),
            default=Value(0.0),
            output_field=FloatField()
        )
    )
    return teams_qs


def limit_to_teams_with_B1G_rpi_and_games_this_season(teams_qs):
    teams_qs = teams_qs.filter(
        rpi_rank__isnull=False
    ).filter(
        Q(wins__gt=0) | Q(losses__gt=0)
    )    
    return teams_qs