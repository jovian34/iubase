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
from player_tracking.models import Player

from live_game_blog.tests.fixtures import teams

from accounts.models import CustomUser
from accounts.tests.fixtures import (
    user_not_logged_in,
    user_iubase17,
    logged_user_schwarbs,
)

this_year = date.today().year


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
            "hsgrad_year": [f"{this_year - 6}"],
            "high_school": ["Tallmadge"],
            "home_city": ["Tallmadge"],
            "home_state": ["OH"],
            "home_country": ["USA"],
            "headshot": [
                "https://www.prepbaseballreport.com/passets/photo/OH/8542307196-PhillipGlasser.png"
            ],
            "birthdate": [f"{this_year - 25}-12-03"],
            "bats": ["Left"],
            "throws": ["Right"],
            "height": [72],
            "weight": [170],
            "trans_event": ["Verbal Commitment from College"],
            "trans_date": [f"{this_year - 3}-06-15"],
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
            "hsgrad_year": [f"{this_year - 6}"],
            "high_school": ["Tallmadge"],
            "home_city": ["Tallmadge"],
            "home_state": ["OH"],
            "home_country": ["USA"],
            "headshot": [
                "https://www.prepbaseballreport.com/passets/photo/OH/8542307196-PhillipGlasser.png"
            ],
            "birthdate": [f"{this_year - 25}-12-03"],
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
            args=[annual_rosters.dt_fresh.player.pk],
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
            args=[annual_rosters.dt_fresh.player.pk],
        )
    )
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)
    assert "Summer Ball:" in str(response.content)
    assert f"{this_year}: USA Collegiate National Team of the International Friendship League" in str(
        response.content
    )


@pytest.mark.django_db
def test_player_rosters_renders_transfer_player_old_team(client, annual_rosters):
    response = client.get(
        reverse(
            "player_rosters",
            args=[annual_rosters.nm_soph.player.pk],
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
            args=[players.nick_mitchell.pk],
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
            args=[players.nick_mitchell.pk],
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
            args=[players.nick_mitchell.pk],
        )
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_transaction_partial_get_redirects_not_logged_in(client, players, teams):
    response = client.get(
        reverse(
            "add_transaction",
            args=[players.nick_mitchell.pk],
        )
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_roster_year_partial_post_adds_roster_year(
    client, players, teams, annual_rosters, logged_user_schwarbs
):
    response = client.post(
        reverse("add_roster_year", args=[players.nick_mitchell.pk]),
        {
            "spring_year": [f"{this_year - 2}"],
            "team": [str(teams.duke.pk)],
            "jersey": ["29"],
            "status": ["Spring Roster"],
            "primary_position": ["Centerfield"],
            "secondary_position": [],
        },
        follow=True,
    )
    assert response.status_code == 200
    assert f"{this_year} Indiana" in str(response.content)
    assert f"{this_year - 1} Miami (Ohio)" in str(response.content)
    assert f"{this_year - 2} Duke" in str(response.content)


@pytest.mark.django_db
def test_add_transaction_partial_post_adds_transaction(
    client, players, teams, annual_rosters, logged_user_schwarbs, prof_orgs
):
    response = client.post(
        reverse("add_transaction", args=[players.brayden_risedorph.pk]),
        {
            "trans_event": ["Drafted"],
            "trans_date": [str(date(this_year, 7, 17))],
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
    response = client.get(reverse("drafted_players", args=[f"{this_year}"]))
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
        reverse("add_roster_year", args=[players.nick_mitchell.pk]),
        {
            "spring_year": [f"{this_year - 2}"],
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
    response = client.get(reverse("fall_depth_chart", args=[f"{this_year - 1}"]))
    assert response.status_code == 200
    assert "Corner Outfield" in str(response.content)
    assert f"Fall {this_year - 1} Available Depth Chart" in str(response.content)
    assert "Devin Taylor" in str(response.content)
    assert "Brayden" not in str(response.content)


@pytest.mark.django_db
def test_spring_depth_chart_renders_indiana_players(
    client, players, teams, annual_rosters
):
    response = client.get(reverse("spring_depth_chart", args=[f"{this_year - 1}"]))
    assert response.status_code == 200
    assert "Catcher" in str(response.context)
    assert f"Spring {this_year - 1} Available Depth Chart" in str(response.content)
    assert "Devin Taylor" in str(response.content)
    assert "Nick" not in str(response.content)  # on different team


@pytest.mark.django_db
def test_fall_roster_renders(client, players, teams, annual_rosters):
    response = client.get(reverse("fall_roster", args=[f"{this_year - 1}"]))
    print(response.content)
    assert response.status_code == 200
    assert "Total Roster Length: 4" in str(response.content)
    assert f"Fall {this_year - 1} Roster" in str(response.content)
    assert "Nathan Ball" in str(response.content)
    assert "Nick Mitchell" in str(response.content)
    assert "Jack Moffitt" in str(response.content)
    assert "Brayden" not in str(response.content)


@pytest.mark.django_db
def test_spring_roster_renders(client, players, teams, annual_rosters):
    response = client.get(reverse("spring_roster", args=[f"{this_year - 1}"]))
    assert response.status_code == 200
    assert "Total Roster Length: 2" in str(response.content)
    assert f"Spring {this_year - 1} Roster" in str(response.content)
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
def test_set_player_properties_produces_correct_end_date_typical_case(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    devin = Player.objects.get(pk=players.devin_taylor.pk)
    assert not devin.first_spring or devin.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    devin = Player.objects.get(pk=players.devin_taylor.pk)
    assert devin.first_spring == this_year - 1
    assert devin.last_spring == this_year + 2


@pytest.mark.django_db
def test_set_player_properties_produces_correct_html_output(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    assert "Devin Taylor (None-None)" in str(response.content)
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("players"), follow=True)
    # see test_set_player_properties_produces_correct_end_date_typical_case for correct year values
    assert f"Devin Taylor ({this_year - 1}-{this_year + 2})" in str(response.content)


@pytest.mark.django_db
def test_set_player_properties_produces_correct_end_date_drafted(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    nick = Player.objects.get(pk=players.nick_mitchell.pk)
    assert not nick.first_spring or nick.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    nick = Player.objects.get(pk=players.nick_mitchell.pk)
    assert nick.first_spring == this_year
    assert nick.last_spring == this_year


@pytest.mark.django_db
def test_set_player_properties_produces_correct_end_date_redshirt_transfer(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    cole = Player.objects.get(pk=players.cole_gilley.pk)
    assert not cole.first_spring or cole.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    cole = Player.objects.get(pk=players.cole_gilley.pk)
    assert cole.first_spring == this_year + 1
    assert cole.last_spring == this_year + 1


@pytest.mark.django_db
def test_set_player_properties_ends_portal_entrant_immediately(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    brooks = Player.objects.get(pk=players.brooks_ey.pk)
    assert not brooks.first_spring or brooks.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    brooks = Player.objects.get(pk=players.brooks_ey.pk)
    assert brooks.first_spring == this_year
    assert brooks.last_spring == this_year


@pytest.mark.django_db
def test_set_player_properties_properly_limits_redshirt_years(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    """
    Jack was rostered at "Duke" for four years, but was injured for the
    first three of those. In the fixture he is given a clock waiver in year two
    This is often assigned retroactively by the NCAA
    Without this he would end this year. If the logic allowed more than one
    redshirt normally he would end in two years.
    """
    response = client.get(reverse("players"), follow=True)
    jack = Player.objects.get(pk=players.jack_moffitt.pk)
    assert not jack.first_spring or jack.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    jack = Player.objects.get(pk=players.jack_moffitt.pk)
    assert jack.first_spring == this_year
    assert jack.last_spring == this_year + 1


@pytest.mark.django_db
def test_set_player_properties_properly_ends_eligible_player_who_is_now_staff(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    """
    Nathan Ball is a freshman player in this test who fails to make 
    the spring roster, and becomes a manager instead.
    """
    response = client.get(reverse("players"), follow=True)
    nate = Player.objects.get(pk=players.nate_ball.pk)
    assert not nate.first_spring or nate.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    nate = Player.objects.get(pk=players.nate_ball.pk)
    assert nate.first_spring == this_year
    assert nate.last_spring == this_year


@pytest.mark.django_db
def test_set_player_properties_properly_resets_drafted_not_signed(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    grant = Player.objects.get(pk=players.grant_hollister.pk)
    assert not grant.first_spring or grant.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    grant = Player.objects.get(pk=players.grant_hollister.pk)
    assert grant.first_spring == this_year + 1
    assert grant.last_spring == this_year + 4


@pytest.mark.django_db
def test_set_player_properties_properly_sets_start_for_early_juco_commit(
    client, players, annual_rosters, transactions, logged_user_schwarbs
):
    response = client.get(reverse("players"), follow=True)
    holton = Player.objects.get(pk=players.holton_compton.pk)
    assert not holton.first_spring or holton.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    holton = Player.objects.get(pk=players.holton_compton.pk)
    assert holton.first_spring == this_year + 1
    assert holton.last_spring == this_year + 2


@pytest.mark.django_db
def test_set_player_properties_asks_for_password_not_logged_in(
    client, players, annual_rosters, transactions
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    assert "Password" in str(response.content)


@pytest.mark.django_db
def test_projected_roster_renders_current_players(
    client, players, transactions, mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert f"Projected Players For Fall {this_year}" in str(response.content)
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_projected_roster_excludes_transfer_portal_entrants(
    client, players, transactions, mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert "Brooks Ey" not in str(response.content)


@pytest.mark.django_db
def test_projected_roster_for_bad_year_redirects_to_pt_index(client):
    response = client.get(reverse("projected_players_fall", args=[f"{this_year + 1}"]))
    assert response.status_code == 302
    response = client.get(reverse("projected_players_fall", args=[f"{this_year + 1}"]), follow=True)
    assert response.status_code == 200
    assert f"{str(timezone.now().year)} Depth Chart" in str(response.content)
    response = client.get(reverse("projected_players_fall", args=[f"{this_year - 1}"]))
    assert response.status_code == 302
    response = client.get(reverse("projected_players_fall", args=[f"{this_year - 1}"]), follow=True)
    assert response.status_code == 200
    assert f"{str(timezone.now().year)} Depth Chart" in str(response.content)


@pytest.mark.django_db
def test_projected_roster_includes_high_school_commit(
    client, players, transactions, mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert "Grant Hollister" in str(response.content)


@pytest.mark.django_db
def test_projected_roster_includes_transfer_commit(
    client, players, transactions, mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert "Holton Compton" in str(response.content)


@pytest.mark.django_db
def test_non_existent_draft_year_redirects_to_index(
    client, players, transactions, mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(
        reverse("projected_players_fall", args=[f"{this_year - 1}"]),
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
    nick = Player.objects.get(pk=players.nick_mitchell.pk)
    assert not nick.first_spring or nick.last_spring
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("players"), follow=True)
    nick = Player.objects.get(pk=players.nick_mitchell.pk)
    assert nick.first_spring == this_year
    assert nick.last_spring == this_year


@pytest.mark.django_db
def test_draft_combine_attendees_renders(
    client, players, transactions, annual_rosters, mlb_draft_date
):
    response = client.get(reverse("draft_combine_attendees", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert response.context["count"] == 2
    for item in ["Nick Mitchell", "College", "Hollister", "Freshman"]:
        assert item in str(response.content)


@pytest.mark.django_db
def test_add_summer_assignment_get_redirects_not_logged_in(client, players, summer_leagues, summer_teams):
    response = client.get(
        reverse("add_summer_assignment", args=[players.devin_taylor]),
        follow=True,
    )
    assert response.status_code == 200
    assert "Password" in str(response.content)


@pytest.mark.django_db
def test_add_summer_assignment_get_renders_form(client, players, summer_leagues, summer_teams, logged_user_schwarbs):
    response = client.get(
        reverse("add_summer_assignment", args=[str(players.devin_taylor.pk)])
    )
    assert response.status_code == 200
    assert "Summer Year" in str(response.content)


@pytest.mark.django_db
def test_add_summer_assignment_post_adds_assignment(client, players, summer_leagues, summer_teams, logged_user_schwarbs):
    response = client.post(
        reverse("add_summer_assignment", args=[str(players.brayden_risedorph.pk)]),
        {
            "summer_year": [f"{this_year}"],
            "summer_team": [str(summer_teams.gb.pk)],
            "summer_league": [str(summer_leagues.nw.pk)],
        },
        follow=True,
    )
    assert response.status_code == 200
    assert "Green Bay" in str(response.content)


@pytest.mark.django_db
def test_summer_assignments_page_renders(client, players, summer_assign, summer_leagues, summer_teams):
    response = client.get(reverse("summer_assignments", args=[f"{this_year}"]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_drafted_players_renders_drafted_not_signed(
    client, players, prof_orgs, transactions, annual_rosters, mlb_draft_date
):
    response = client.get(reverse("drafted_players", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert "Grant Hollister" in str(response.content)
    assert response.context["count"] == 2
    assert "High School Signee" in str(response.content)
    assert "IU Player/Alumni" in str(response.content)
    assert "He is expected by insiders to require $500,000 to sign." in str(response.content)
    assert "$400,100 before" not in str(response.content)
    assert "Philadelphia Phillies incur" not in str(response.content)

@pytest.mark.django_db
def test_drafted_players_renders_signed(
    client, players, prof_orgs, transactions, annual_rosters, mlb_draft_date
):
    response = client.get(reverse("drafted_players", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert response.context["count"] == 2
    assert "Nick Mitchell signed a professional contract with a bonus of $367,000." in str(response.content)
    assert "This bonus was 92% of the assigned value of the draft pick." in str(response.content)
    assert "Bonus value was reported two days after signing." in str(response.content)


@pytest.mark.django_db
def test_drafted_players_renders_unsigned(
    client, players, prof_orgs, transactions, annual_rosters, mlb_draft_date
):
    response = client.get(reverse("drafted_players", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert "Grant Hollister did not sign and will be on campus in the fall." in str(response.content)


    