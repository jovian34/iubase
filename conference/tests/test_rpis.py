import pytest

from bs4 import BeautifulSoup
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


@pytest.mark.django_db
def test_store_b1g_rpi_data_updates_existing_rank_without_duplicate(
    monkeypatch,
    teams,
):
    spring_year = 2026
    conf_models.TeamRpi.objects.create(
        team=teams.indiana,
        rpi_rank=68,
        spring_year=spring_year,
    )
    monkeypatch.setattr(
        rpis,
        "make_b1G_rpi_dict",
        lambda requested_year: {"Indiana": 42},
    )

    rpis.store_b1g_rpi_data_in_database(spring_year)

    indiana_rpis = conf_models.TeamRpi.objects.filter(
        team=teams.indiana,
        spring_year=spring_year,
    )
    assert indiana_rpis.count() == 1
    assert indiana_rpis.get().rpi_rank == 42


def test_parse_table_raises_clear_error_when_stats_table_is_missing(monkeypatch):
    page_without_stats = BeautifulSoup(
        "<html><body><p>Conference data unavailable</p></body></html>",
        "html.parser",
    )
    monkeypatch.setattr(
        rpis,
        "request_table_into_parser",
        lambda spring_year: page_without_stats,
    )

    with pytest.raises(RuntimeError, match="Stats table not found"):
        rpis.parse_table(2026)
