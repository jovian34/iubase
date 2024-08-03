import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import date, datetime

from player_tracking.tests.fixtures.annual_rosters import annual_rosters
from player_tracking.tests.fixtures.mlb_draft_date import mlb_draft_date
from player_tracking.tests.fixtures.players import players
from player_tracking.tests.fixtures.prof_org import prof_orgs
from player_tracking.tests.fixtures.transactions import transactions
from player_tracking.tests.fixtures.summer import (
    summer_assign,
    summer_leagues,
    summer_teams,
)

from live_game_blog.tests.fixtures import teams

from accounts.models import CustomUser
from accounts.tests.fixtures import (
    user_not_logged_in,
    user_iubase17,
    logged_user_schwarbs,
)


@pytest.mark.django_db
def test_index(client, players):
    response = client.get(reverse("players"))
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_add_player_form_renders(client, logged_user_schwarbs):
    response = client.get(reverse("add_player"))
    assert response.status_code == 200
    assert "First Name" in str(response.content)
    assert "Headshot or other photo file URL" in str(response.content)


@pytest.mark.django_db
def test_add_player_form_redirects_not_logged_in(client):
    response = client.get(reverse("add_player"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_player_form_adds_new_player(client, players, logged_user_schwarbs):
    response = client.post(
        reverse("add_player"),
        {
            "first": ["Phillip"],
            "last": ["Glasser"],
            "hsgrad_year": ["2018"],
            "high_school": ["Tallmadge"],
            "home_city": ["Tallmadge"],
            "home_state": ["OH"],
            "home_country": ["USA"],
            "headshot": [
                "https://www.prepbaseballreport.com/passets/photo/OH/8542307196-PhillipGlasser.png"
            ],
            "birthdate": ["1999-12-03"],
            "bats": ["Left"],
            "throws": ["Right"],
            "height": [72],
            "weight": [170],
            "trans_event": ["Verbal Commitment from College"],
            "trans_date": ["2021-06-15"],
            "primary_position": ["Shortstop"],
            "citation": [
                "https://d1baseball.com/transfers/2021-22-d1baseball-transfer-tracker/"
            ],
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Phillip Glasser" in str(response.content)


@pytest.mark.django_db
def test_add_player_form_asks_for_password_not_logged_in(client, players):
    response = client.post(
        reverse("add_player"),
        {
            "first": ["Phillip"],
            "last": ["Glasser"],
            "hsgrad_year": ["2018"],
            "high_school": ["Tallmadge"],
            "home_city": ["Tallmadge"],
            "home_state": ["OH"],
            "home_country": ["USA"],
            "headshot": [
                "https://www.prepbaseballreport.com/passets/photo/OH/8542307196-PhillipGlasser.png"
            ],
            "birthdate": ["1999-12-03"],
            "bats": ["Left"],
            "throws": ["Right"],
            "height": [72],
            "weight": [170],
            "clock": [5],
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Password" in str(response.content)


@pytest.mark.django_db
def test_player_rosters_renders_one_player_only(client, annual_rosters):
    response = client.get(
        reverse(
            "player_rosters",
            args=[annual_rosters.dt_2023.player.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)
    assert "Nick" not in str(response.content)


@pytest.mark.django_db
def test_player_rosters_renders_summer_teams(
    client, annual_rosters, summer_assign, summer_leagues, summer_teams
):
    response = client.get(
        reverse(
            "player_rosters",
            args=[annual_rosters.dt_2023.player.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)
    assert "Summer Ball:" in str(response.content)
    assert "2024: USA Collegiate National Team of the International Friendship League" in str(
        response.content
    )


@pytest.mark.django_db
def test_player_rosters_renders_transfer_player_old_team(client, annual_rosters):
    response = client.get(
        reverse(
            "player_rosters",
            args=[annual_rosters.nm_2023.player.pk],
        )
    )
    assert response.status_code == 200
    assert "Nick Mitchell" in str(response.content)
    assert "Devin" not in str(response.content)
    assert "Miami (Ohio)" in str(response.content)


@pytest.mark.django_db
def test_add_roster_year_partial_get_renders_form_fields(
    client, players, teams, logged_user_schwarbs
):
    response = client.get(
        reverse(
            "add_roster_year",
            args=[players.nm2021.pk],
        )
    )
    assert response.status_code == 200
    assert "Spring Year" in str(response.content)
    assert "Indiana" in str(response.content)
    assert str(timezone.now().year) in str(response.content)


@pytest.mark.django_db
def test_add_transaction_partial_get_renders_form_fields(
    client, players, teams, logged_user_schwarbs
):
    response = client.get(
        reverse(
            "add_transaction",
            args=[players.nm2021.pk],
        )
    )
    assert response.status_code == 200
    assert "Transaction Event" in str(response.content)
    assert "Transaction Date" in str(response.content)
    assert str(timezone.now().year) in str(response.content)


@pytest.mark.django_db
def test_add_roster_year_partial_get_redirects_not_logged_in(client, players, teams):
    response = client.get(
        reverse(
            "add_roster_year",
            args=[players.nm2021.pk],
        )
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_transaction_partial_get_redirects_not_logged_in(client, players, teams):
    response = client.get(
        reverse(
            "add_transaction",
            args=[players.nm2021.pk],
        )
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_roster_year_partial_post_adds_roster_year(
    client, players, teams, annual_rosters, logged_user_schwarbs
):
    response = client.post(
        reverse("add_roster_year", args=[players.nm2021.pk]),
        {
            "spring_year": [2022],
            "team": [str(teams.duke.pk)],
            "jersey": [29],
            "status": ["Spring Roster"],
            "primary_position": ["Centerfield"],
            "secondary_position": [],
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "2024 Indiana" in str(response.content)
    assert "2023 Miami (Ohio)" in str(response.content)
    assert "2022 Duke" in str(response.content)


@pytest.mark.django_db
def test_add_transaction_partial_post_adds_transaction(
    client, players, teams, annual_rosters, logged_user_schwarbs, prof_orgs
):
    response = client.post(
        reverse("add_transaction", args=[players.br2022.pk]),
        {
            "trans_event": ["Drafted"],
            "trans_date": [str(date(2024, 7, 17))],
            "citation": ["https://www.mlb.com/draft/tracker"],
            "other_team": [],
            "prof_org": [prof_orgs.d_backs.pk],
            "bonus_or_slot": ["150000"],
            "comment": ["Expected to go over slot value."]
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Drafted" in str(response.content)
    assert "July 17" in str(response.content)
    assert 'href="https://www.mlb.com/draft/tracker"'
    response = client.get(reverse("drafted_players", args=["2024"]))
    assert response.status_code == 200
    assert "Brayden Risedorph" in str(response.content)
    assert "he can get a bonus value of $150,000" in str(response.content)
    assert "Expected to go over slot value." in str(response.content)
    assert "Arizona Diamondbacks" in str(response.content)



@pytest.mark.django_db
def test_add_roster_year_partial_post_asks_for_password_not_logged_in(
    client, players, teams, annual_rosters
):
    response = client.post(
        reverse("add_roster_year", args=[players.nm2021.pk]),
        {
            "spring_year": [2022],
            "team": [str(teams.duke.pk)],
            "jersey": [29],
            "status": ["Spring Roster"],
            "primary_position": ["Centerfield"],
            "secondary_position": [],
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Password" in str(response.content)


@pytest.mark.django_db
def test_pt_index_renders(client):
    response = client.get(reverse("pt_index"))
    assert response.status_code == 200
    assert f"{str(timezone.now().year)} Depth Chart" in str(response.content)


@pytest.mark.django_db
def test_fall_depth_chart_renders(client, players, teams, annual_rosters):
    response = client.get(reverse("fall_depth_chart", args=["2023"]))
    assert response.status_code == 200
    assert "Corner Outfield" in str(response.content)
    assert "Fall 2023 Available Depth Chart" in str(response.content)
    assert "Devin Taylor" in str(response.content)
    assert "Brayden" not in str(response.content)


@pytest.mark.django_db
def test_spring_depth_chart_renders_indiana_players(
    client, players, teams, annual_rosters
):
    response = client.get(reverse("spring_depth_chart", args=["2023"]))
    assert response.status_code == 200
    assert "Catcher" in str(response.context)
    assert "Spring 2023 Available Depth Chart" in str(response.content)
    assert "Devin Taylor" in str(response.content)
    assert "Nick" not in str(response.content)  # on different team


@pytest.mark.django_db
def test_fall_roster_renders(client, players, teams, annual_rosters):
    response = client.get(reverse("fall_roster", args=["2023"]))
    print(response.content)
    assert response.status_code == 200
    assert "Total Roster Length: 4" in str(response.content)
    assert "Fall 2023 Roster" in str(response.content)
    assert "Nathan Ball" in str(response.content)
    assert "Nick Mitchell" in str(response.content)
    assert "Jack Moffitt" in str(response.content)
    assert "Brayden" not in str(response.content)


@pytest.mark.django_db
def test_spring_roster_renders(client, players, teams, annual_rosters):
    response = client.get(reverse("spring_roster", args=["2023"]))
    assert response.status_code == 200
    assert "Total Roster Length: 2" in str(response.content)
    assert "Spring 2023 Roster" in str(response.content)
    assert "Nick Mitchell" not in str(response.content)
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_portal_page_renders(client, players, teams, annual_rosters, transactions):
    current_dt = datetime.now()
    response = client.get(reverse("portal", args=[str(current_dt.year)]))
    assert response.status_code == 200
    assert "Total Players in the Portal: 1"
    assert "Brooks Ey" in str(response.content)
    assert "Devin" not in str(response.content)


@pytest.mark.django_db
def test_set_last_spring_produces_correct_end_date_typical_case(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    assert "Devin Taylor (None-None)" in str(response.content)
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("players"), follow=True)
    assert "Devin Taylor (2023-2026)" in str(response.content)


@pytest.mark.django_db
def test_set_last_spring_produces_correct_end_date_drafted(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    assert "Nick Mitchell (None-None)" in str(response.content)
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("players"), follow=True)
    assert "Nick Mitchell (2024-2024)" in str(response.content)


@pytest.mark.django_db
def test_set_last_spring_produces_correct_end_date_redshirt_transfer(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    assert "Cole Gilley (None-None)" in str(response.content)
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("players"), follow=True)
    assert "Cole Gilley (2025-2025)" in str(response.content)


@pytest.mark.django_db
def test_set_last_spring_ends_portal_entrant_immediately(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    assert "Brooks Ey (None-None)" in str(response.content)
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("players"), follow=True)
    assert "Brooks Ey (2024-2024)" in str(response.content)


@pytest.mark.django_db
def test_set_last_spring_properly_limits_redshirt_years(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    """
    Jack was rostered at "Duke" for four years, but was injured for the
    first three of those. In the fixture he is given a clock waiver in year two
    This is often assigned retroactively by the NCAA
    Without this he would end in 2024. If the logic allowed more than one
    redshirt normally he would end in 2026.
    """
    response = client.get(reverse("players"), follow=True)
    assert "Jack Moffitt (None-None)" in str(response.content)
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("players"), follow=True)
    assert "Jack Moffitt (2024-2025)" in str(response.content)


@pytest.mark.django_db
def test_set_last_spring_properly_ends_eligible_player_who_is_now_staff(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    """
    Nathan Ball is a freshman player in this test who fails to make 
    the spring roster, and becomes a manager instead.
    """
    response = client.get(reverse("players"), follow=True)
    assert "Nathan Ball (None-None)" in str(response.content)
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("players"), follow=True)
    assert "Nathan Ball (2024-2024)" in str(response.content)


@pytest.mark.django_db
def test_set_last_spring_properly_resets_drafted_not_signed(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    assert "Grant Hollister (None-None)" in str(response.content)
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("players"), follow=True)
    assert "Grant Hollister (2025-2028)" in str(response.content)


@pytest.mark.django_db
def test_set_last_spring_properly_sets_start_for_early_juco_commit(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    assert "Holton Compton (None-None)" in str(response.content)
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("players"), follow=True)
    assert "Holton Compton (2025-2026)" in str(response.content)


@pytest.mark.django_db
def test_set_last_spring_asks_for_password_not_logged_in(
    client, players, annual_rosters, transactions
):
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    assert "Password" in str(response.content)


@pytest.mark.django_db
def test_projected_roster_renders_current_players(
    client, players, transactions, mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall", args=["2024"]))
    assert response.status_code == 200
    assert "Projected Players For Fall 2024" in str(response.content)
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_projected_roster_excludes_transfer_portal_entrants(
    client, players, transactions, mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall", args=["2024"]))
    assert response.status_code == 200
    assert "Brooks Ey" not in str(response.content)


@pytest.mark.django_db
def test_projected_roster_for_bad_year_redirects_to_pt_index(client):
    response = client.get(reverse("projected_players_fall", args=["2025"]))
    assert response.status_code == 302
    response = client.get(reverse("projected_players_fall", args=["2025"]), follow=True)
    assert response.status_code == 200
    assert f"{str(timezone.now().year)} Depth Chart" in str(response.content)
    response = client.get(reverse("projected_players_fall", args=["2023"]))
    assert response.status_code == 302
    response = client.get(reverse("projected_players_fall", args=["2023"]), follow=True)
    assert response.status_code == 200
    assert f"{str(timezone.now().year)} Depth Chart" in str(response.content)


@pytest.mark.django_db
def test_projected_roster_includes_high_school_commit(
    client, players, transactions, mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall", args=["2024"]))
    assert response.status_code == 200
    assert "Grant Hollister" in str(response.content)


@pytest.mark.django_db
def test_projected_roster_includes_transfer_commit(
    client, players, transactions, mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall", args=["2024"]))
    assert response.status_code == 200
    assert "Holton Compton" in str(response.content)


@pytest.mark.django_db
def test_non_existent_draft_year_redirects_to_index(
    client, players, transactions, mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    response = client.get(
        reverse("projected_players_fall", args=["2023"]),
        follow=True,
    )
    assert response.status_code == 200
    assert "Grant Hollister" not in str(response.content)
    assert "Player Tracking" in str(response.content)


@pytest.mark.django_db
def test_draft_combine_attendees_set_to_current_last_year(
    client, players, transactions, annual_rosters, mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    assert "Nick Mitchell (None-None)" in str(response.content)
    response = client.get(reverse("calc_last_spring"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("players"), follow=True)
    assert "Nick Mitchell (2024-2024)" in str(response.content)


@pytest.mark.django_db
def test_draft_combine_attendees_renders(
    client, players, transactions, annual_rosters, mlb_draft_date
):
    response = client.get(reverse("draft_combine_attendees", args=["2024"]))
    assert response.status_code == 200
    assert "Nick Mitchell" in str(response.content)
    assert "Count of Players: 2" in str(response.content)
    assert "College" in str(response.content)
    assert "Hollister" in str(response.content)
    assert "Freshman" in str(response.content)


@pytest.mark.django_db
def test_add_summer_assignment_get_redirects_not_logged_in(client, players, summer_leagues, summer_teams):
    response = client.get(
        reverse("add_summer_assignment", args=[players.dt2022]),
        follow=True,
    )
    assert response.status_code == 200
    assert "Password" in str(response.content)


@pytest.mark.django_db
def test_add_summer_assignment_get_renders_form(client, players, summer_leagues, summer_teams, logged_user_schwarbs):
    response = client.get(
        reverse("add_summer_assignment", args=[str(players.dt2022.pk)])
    )
    assert response.status_code == 200
    assert "Summer Year" in str(response.content)


@pytest.mark.django_db
def test_add_summer_assignment_post_adds_assignment(client, players, summer_leagues, summer_teams, logged_user_schwarbs):
    response = client.post(
        reverse("add_summer_assignment", args=[str(players.br2022.pk)]),
        {
            "summer_year": [2024],
            "summer_team": [str(summer_teams.gb.pk)],
            "summer_league": [str(summer_leagues.nw.pk)],
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Green Bay" in str(response.content)


@pytest.mark.django_db
def test_summer_assignments_page_renders(client, players, summer_assign, summer_leagues, summer_teams):
    response = client.get(reverse("summer_assignments", args=["2024"]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_drafted_players_renders_drafted_not_signed(
    client, players, prof_orgs, transactions, annual_rosters, mlb_draft_date
):
    response = client.get(reverse("drafted_players", args=["2024"]))
    assert response.status_code == 200
    assert "Grant Hollister" in str(response.content)
    assert "Count of Players: 2" in str(response.content)
    assert "He is expected by insiders to require $500,000 to sign." in str(response.content)
    assert "$400,100 before" not in str(response.content)
    assert "Philadelphia Phillies incur" not in str(response.content)

@pytest.mark.django_db
def test_drafted_players_renders_signed(
    client, players, prof_orgs, transactions, annual_rosters, mlb_draft_date
):
    response = client.get(reverse("drafted_players", args=["2024"]))
    assert response.status_code == 200
    assert "Count of Players: 2" in str(response.content)
    assert "Nick Mitchell signed a professional contract with a bonus of $367,000." in str(response.content)
    assert "This bonus was 92% of the assigned value of the draft pick." in str(response.content)
    assert "Bonus value was reported two days after signing." in str(response.content)


@pytest.mark.django_db
def test_drafted_players_renders_unsigned(
    client, players, prof_orgs, transactions, annual_rosters, mlb_draft_date
):
    response = client.get(reverse("drafted_players", args=["2024"]))
    assert response.status_code == 200
    assert "Grant Hollister did not sign and will be on campus in the fall." in str(response.content)


    