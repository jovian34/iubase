from datetime import date

import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from accounts.tests.fixtures import logged_user_schwarbs
from live_game_blog.tests.fixtures.teams import teams
from player_tracking.models import Accolade, AnnualRoster
from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.players import players


this_year = date.today().year


def enter_red_belts(
    admin_client,
    *,
    spring_year,
    award_date,
    pitcher,
    hitter,
    defender,
):
    response = admin_client.post(
        reverse("red_belt_entry", args=[spring_year]),
        {
            "award_date": award_date,
            "citation": "https://example.com/talking-hoosier-baseball/red-belts",
            "pitcher": pitcher.pk,
            "hitter": hitter.pk,
            "defender": defender.pk,
        },
    )
    assert response.status_code == 302


def leaderboard_rows(response, heading):
    page = BeautifulSoup(response.content, "html.parser")
    table = page.find("h2", string=heading).find_next("table")
    return [
        [cell.get_text(" ", strip=True) for cell in row.find_all("td")]
        for row in table.find_all("tr")
    ]


@pytest.mark.django_db
def test_red_belt_leaderboard_page_renders(admin_client):
    response = admin_client.get(reverse("red_belt_leaderboard", args=[this_year]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_red_belt_leaderboard_includes_only_weekly_awards_from_entry_form(
    admin_client, annual_rosters
):
    spring_year = this_year - 1
    enter_red_belts(
        admin_client,
        spring_year=spring_year,
        award_date=date(spring_year, 3, 1),
        pitcher=annual_rosters.rk_soph,
        hitter=annual_rosters.dt_fresh,
        defender=annual_rosters.br_fresh,
    )
    Accolade.objects.create(
        player=annual_rosters.rk_soph.player,
        annual_roster=annual_rosters.rk_soph,
        award_date=date(spring_year, 3, 2),
        citation="https://example.com/non-weekly-red-belt",
        name="Joey DeNato Red Belt for pitching",
        award_org="Talking Hoosier Baseball",
    )

    response = admin_client.get(reverse("red_belt_leaderboard", args=[spring_year]))

    assert list(response.context["denato_leaders"]) == [
        {
            "player__id": annual_rosters.rk_soph.player_id,
            "player__first": "Ryan",
            "player__last": "Kraft",
            "award_count": 1,
        }
    ]
    assert list(response.context["dickerson_leaders"]) == [
        {
            "player__id": annual_rosters.dt_fresh.player_id,
            "player__first": "Devin",
            "player__last": "Taylor",
            "award_count": 1,
        }
    ]
    assert list(response.context["butler_leaders"]) == [
        {
            "player__id": annual_rosters.br_fresh.player_id,
            "player__first": "Brayden",
            "player__last": "Risedorph",
            "award_count": 1,
        }
    ]


@pytest.mark.django_db
def test_red_belt_leaderboard_separates_weekly_awards_by_year(
    admin_client, annual_rosters
):
    previous_year = this_year - 1
    enter_red_belts(
        admin_client,
        spring_year=previous_year,
        award_date=date(previous_year, 3, 1),
        pitcher=annual_rosters.rk_soph,
        hitter=annual_rosters.dt_fresh,
        defender=annual_rosters.br_fresh,
    )
    enter_red_belts(
        admin_client,
        spring_year=this_year,
        award_date=date(this_year, 3, 1),
        pitcher=annual_rosters.jm2024,
        hitter=annual_rosters.rk_jr,
        defender=annual_rosters.dt_soph,
    )

    previous_response = admin_client.get(
        reverse("red_belt_leaderboard", args=[previous_year])
    )
    current_response = admin_client.get(
        reverse("red_belt_leaderboard", args=[this_year])
    )

    assert {
        row["player__first"] for row in previous_response.context["denato_leaders"]
    } == {"Ryan"}
    assert {
        row["player__first"] for row in current_response.context["denato_leaders"]
    } == {"Jack"}
    assert {
        row["player__first"] for row in previous_response.context["dickerson_leaders"]
    } == {"Devin"}
    assert {
        row["player__first"] for row in current_response.context["dickerson_leaders"]
    } == {"Ryan"}
    assert {
        row["player__first"] for row in previous_response.context["butler_leaders"]
    } == {"Brayden"}
    assert {
        row["player__first"] for row in current_response.context["butler_leaders"]
    } == {"Devin"}


@pytest.mark.django_db
def test_red_belt_leaderboard_displays_weekly_award_totals_in_tables(
    admin_client, annual_rosters
):
    spring_year = this_year - 1
    for award_day in (1, 8):
        enter_red_belts(
            admin_client,
            spring_year=spring_year,
            award_date=date(spring_year, 3, award_day),
            pitcher=annual_rosters.rk_soph,
            hitter=annual_rosters.dt_fresh,
            defender=annual_rosters.br_fresh,
        )

    response = admin_client.get(reverse("red_belt_leaderboard", args=[spring_year]))

    assert leaderboard_rows(response, "Joey DeNato Pitching Red Belts") == [
        ["Ryan Kraft", "2"]
    ]
    assert leaderboard_rows(response, "Alex Dickerson Hitting Red Belts") == [
        ["Devin Taylor", "2"]
    ]
    assert leaderboard_rows(response, "Tony Butler Defense Red Belts") == [
        ["Brayden Risedorph", "2"]
    ]


@pytest.mark.django_db
def test_red_belt_leaderboard_lists_players_with_most_awards_first(
    admin_client, annual_rosters
):
    spring_year = this_year - 1
    for award_day, pitcher in (
        (1, annual_rosters.rk_soph),
        (8, annual_rosters.br_fresh),
        (15, annual_rosters.rk_soph),
    ):
        enter_red_belts(
            admin_client,
            spring_year=spring_year,
            award_date=date(spring_year, 3, award_day),
            pitcher=pitcher,
            hitter=annual_rosters.dt_fresh,
            defender=annual_rosters.br_fresh,
        )

    response = admin_client.get(reverse("red_belt_leaderboard", args=[spring_year]))

    assert leaderboard_rows(response, "Joey DeNato Pitching Red Belts") == [
        ["Ryan Kraft", "2"],
        ["Brayden Risedorph", "1"],
    ]
