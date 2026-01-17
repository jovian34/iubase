import pytest

from django.db.models import Q

from conference.logic import rpis
from conference import models as conf_models

from live_game_blog.tests.fixtures.teams import teams


@pytest.mark.django_db
def test_store_b1g_rpi_data_in_database_stores_2025_values(teams):
    rpis.store_b1g_rpi_data_in_database("2025")
    wash_rpi = conf_models.TeamRpi.objects.get(
        Q(spring_year=2025) & Q(team__team_name="Washington")
    )
    assert wash_rpi.rpi_rank == 78
    iu_rpi = conf_models.TeamRpi.objects.get(
        Q(spring_year=2025) & Q(team__team_name="Indiana")
    )
    assert iu_rpi.rpi_rank == 68
    ill_rpi = conf_models.TeamRpi.objects.get(
        Q(spring_year=2025) & Q(team__team_name="Illinois")
    )
    assert ill_rpi.rpi_rank == 115
    ucla_rpi = conf_models.TeamRpi.objects.get(
        Q(spring_year=2025) & Q(team__team_name="UCLA")
    )
    assert ucla_rpi.rpi_rank == 10
