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
def test_all_players_renders(client, players):
    response = client.get(reverse("players"))
    assert response.status_code == 200
    assert "Devin Taylor" in str(response.content)


@pytest.mark.django_db
def test_all_players_renders_in_alpha_order_by_last_name(client, players):
    response = client.get(reverse("players"))
    assert response.status_code == 200
    output = str(response.content)
    nb = output.find("Nate Ball")
    br = output.find("Brayden Risedorph")
    assert br > nb


@pytest.mark.django_db
def test_all_players_renders_in_alpha_order_by_case_insensitive_last_name(client, players):
    '''
    Edge case where player's last name starts with a lower case letter
    The order_by function normally orders capital letters before lower case
    a Lower() method is applied to make the ordering case insensative
    '''
    response = client.get(reverse("players"))
    assert response.status_code == 200
    output = str(response.content)
    oo = output.find("Owen ten Oever")
    aw = output.find("Andrew Wiggins")
    assert aw > oo


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
    assert response.status_code == 200
    assert "Total Roster Length: 4" in str(response.content)
    assert f"Fall {this_year - 1} Roster" in str(response.content)
    assert "Nathan Ball" in str(response.content)
    assert "Nick Mitchell" in str(response.content)
    assert "Jack Moffitt" in str(response.content)
    assert "Brayden" not in str(response.content)


@pytest.mark.django_db
def test_fall_roster_fw_to_instead_of_projection(client, players, teams, annual_rosters):
    response = client.get(reverse("projected_players_fall", args=[f"{this_year - 1}"]))
    assert response.status_code == 302
    response = client.get(reverse("projected_players_fall", args=[f"{this_year - 1}"]), follow=True)
    assert response.status_code == 200
    assert "Total Roster Length: 4" in str(response.content)
    assert f"Fall {this_year - 1} Roster" in str(response.content)
    assert "Nathan Ball" in str(response.content)
    assert "Nick Mitchell" in str(response.content)
    assert "Jack Moffitt" in str(response.content)
    assert "Brayden" not in str(response.content)


@pytest.mark.django_db
def test_fall_players_fw_to_fall_roster_if_exists(client, players, teams, annual_rosters):
    response = client.get(reverse("fall_players", args=[f"{this_year - 1}"]))
    assert response.status_code == 302
    response = client.get(reverse("fall_players", args=[f"{this_year - 1}"]), follow=True)
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
def test_projected_players_for_past_year_redirects_to_pt_index(client):
    response = client.get(reverse("projected_players_fall", args=[f"{this_year - 1}"]))
    assert response.status_code == 302
    response = client.get(reverse("projected_players_fall", args=[f"{this_year - 1}"]), follow=True)
    assert response.status_code == 200
    assert f"{this_year} Depth Chart" in str(response.content)


@pytest.mark.django_db
def test_projected_players_for_future_year_redirects_to_future(client):
    response = client.get(reverse("projected_players_fall", args=[f"{this_year + 1}"]))
    assert response.status_code == 302
    response = client.get(reverse("projected_players_fall", args=[f"{this_year + 1}"]), follow=True)
    assert response.status_code == 200
    assert f"All Eligible Players For Fall {this_year + 1}" in str(response.content)


@pytest.mark.django_db
def test_projected_roster_includes_incoming_high_school_commit(
    client, players, transactions, mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert "Grant Hollister" in str(response.content)


@pytest.mark.django_db
def test_projected_roster_excludes_future_high_school_commit(
    client, players, transactions, mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    assert response.status_code == 200
    response = client.get(reverse("projected_players_fall", args=[f"{this_year}"]))
    assert response.status_code == 200
    assert "Xavier" not in str(response.content)


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


@pytest.mark.django_db
def test_projected_players_future_fall_renders(
    client, players, transactions, mlb_draft_date, logged_user_schwarbs
):
    response = client.get(reverse("set_player_properties"), follow=True)
    response = client.get(reverse("projected_players_future_fall", args=[f"{this_year + 1}"]))
    assert "Grant Hollister" in str(response.content)
    assert "Jack Moffitt" not in str(response.content)
    