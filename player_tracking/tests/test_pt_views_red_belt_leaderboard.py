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


def create_red_belt(roster, award_date, award_name):
    return Accolade.objects.create(
        player=roster.player,
        annual_roster=roster,
        award_date=award_date,
        citation="https://example.com/talking-hoosier-baseball/red-belts",
        name=award_name,
        award_org="Talking Hoosier Baseball",
    )


def create_pitching_red_belt(roster, award_date):
    return create_red_belt(
        roster,
        award_date,
        "Joey DeNato Weekly Red Belt for pitching",
    )


def award_section(response, heading):
    page = BeautifulSoup(response.content, "html.parser")
    return page.find("h2", string=heading).find_parent(
        "div", class_="red-belt-award"
    )


def award_group(section, award_count):
    return section.find(
        "div",
        class_="red-belt-count-group",
        attrs={"data-award-count": str(award_count)},
    )


def award_group_link_names(section, award_count):
    group = award_group(section, award_count)
    return [link.get_text(" ", strip=True) for link in group.find_all("a")]


def single_player_url(player):
    return reverse("single_player_page", args=[player.pk])


def leaderboard_names(leaders):
    return [
        f"{row['player__first']} {row['player__last']}"
        for row in leaders
    ]


@pytest.mark.django_db
def test_red_belt_leaderboard_page_renders(admin_client):
    response = admin_client.get(reverse("red_belt_leaderboard", args=[this_year]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_red_belt_leaderboard_renders_awards_as_separate_divs(admin_client):
    response = admin_client.get(reverse("red_belt_leaderboard", args=[this_year]))
    page = BeautifulSoup(response.content, "html.parser")
    leaderboard = page.find("div", class_="red-belt-leaderboard")
    award_headings = [
        heading.get_text(" ", strip=True)
        for heading in leaderboard.find_all("h2")
    ]

    assert award_headings == [
        "Joey DeNato Pitching Red Belts",
        "Alex Dickerson Hitting Red Belts",
        "Tony Butler Defense Red Belts",
    ]
    assert len(leaderboard.find_all("div", class_="red-belt-award")) == 3


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

    denato_leaders = list(response.context["denato_leaders"])
    dickerson_leaders = list(response.context["dickerson_leaders"])
    butler_leaders = list(response.context["butler_leaders"])

    assert leaderboard_names(denato_leaders) == ["Ryan Kraft"]
    assert leaderboard_names(dickerson_leaders) == ["Devin Taylor"]
    assert leaderboard_names(butler_leaders) == ["Brayden Risedorph"]
    assert denato_leaders[0]["award_count"] == 1
    assert dickerson_leaders[0]["award_count"] == 1
    assert butler_leaders[0]["award_count"] == 1


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
def test_red_belt_leaderboard_groups_players_by_weekly_award_totals(
    admin_client, annual_rosters
):
    spring_year = this_year - 1
    for award_day, pitcher in (
        (1, annual_rosters.rk_soph),
        (3, annual_rosters.br_fresh),
        (8, annual_rosters.br_fresh),
        (15, annual_rosters.rk_soph),
        (22, annual_rosters.rk_soph),
        (29, annual_rosters.hc_fresh),
        (30, annual_rosters.rk_soph),
        (31, annual_rosters.hc_fresh),
        (2, annual_rosters.dt_fresh),
    ):
        create_pitching_red_belt(pitcher, date(spring_year, 3, award_day))

    response = admin_client.get(reverse("red_belt_leaderboard", args=[spring_year]))
    section = award_section(response, "Joey DeNato Pitching Red Belts")

    assert section.find("h3", string="4 Red Belts") is not None
    assert section.find("h3", string="2 Red Belts") is not None
    assert section.find("h3", string="1 Red Belt") is not None
    assert section.find("table") is None
    assert award_group_link_names(section, 4) == ["Ryan Kraft"]
    assert award_group_link_names(section, 2) == [
        "Holton Compton",
        "Brayden Risedorph",
    ]
    assert award_group_link_names(section, 1) == ["Devin Taylor"]


@pytest.mark.django_db
def test_red_belt_leaderboard_features_top_award_group_with_linked_headshots(
    admin_client, annual_rosters
):
    spring_year = this_year - 1
    annual_rosters.rk_soph.player.headshot = (
        "https://example.com/player-headshots/ryan-kraft.jpg"
    )
    annual_rosters.rk_soph.player.save()
    for award_day, pitcher in (
        (1, annual_rosters.rk_soph),
        (8, annual_rosters.rk_soph),
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
    section = award_section(response, "Joey DeNato Pitching Red Belts")
    leaders = award_group(section, 3).find("div", class_="red-belt-leaders")
    leader = leaders.find("figure", class_="red-belt-leader")
    leader_link = leader.find("a")
    leader_image = leader.find("img")

    assert leader_link["href"] == single_player_url(annual_rosters.rk_soph.player)
    assert leader_image["src"] == annual_rosters.rk_soph.player.headshot
    assert leader_image["alt"] == "Ryan Kraft"
    assert leader.find("figcaption").get_text(" ", strip=True) == "Ryan Kraft"


@pytest.mark.django_db
def test_red_belt_leaderboard_links_remaining_grouped_player_names(
    admin_client, annual_rosters
):
    spring_year = this_year - 1
    for award_day, pitcher in (
        (1, annual_rosters.rk_soph),
        (8, annual_rosters.rk_soph),
        (15, annual_rosters.br_fresh),
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
    section = award_section(response, "Joey DeNato Pitching Red Belts")
    group = award_group(section, 1)
    player_link = group.find("li").find("a")

    assert group.find("div", class_="red-belt-leaders") is None
    assert player_link["href"] == single_player_url(annual_rosters.br_fresh.player)
    assert player_link.get_text(" ", strip=True) == "Brayden Risedorph"


def test_red_belt_leaderboard_styles_awards_as_separate_panels():
    style_file = "django_project/static/index/css/style.css"

    with open(style_file) as styles:
        style_rules = styles.read()

    assert ".red-belt-leaderboard" in style_rules
    assert ".red-belt-award" in style_rules
    assert ".red-belt-leaders" in style_rules
    assert ".red-belt-leader img" in style_rules
