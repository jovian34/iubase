import pytest
from django import urls

from conference import year

from live_game_blog.tests.fixtures.teams import teams
from conference.tests.fixtures.conf_series import conf_series
from conference.tests.fixtures.conf_teams import conf_teams
from conference.tests.fixtures.conferences import conferences
from conference.tests.fixtures.team_rpis import team_rpis


@pytest.mark.django_db
def test_standings_page_for_prior_year_renders(client, teams, team_rpis, conf_series, conf_teams, conferences):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()-1]))
    assert response.status_code == 200
    output = response.content.decode()
    assert f"{year.get_spring_year()-1} B1G Standings" in output
    assert "Indiana" in output

    ucla = output.find("UCLA")
    iu = output.find("Indiana")
    nw = output.find("Northwestern")
    rut = output.find("Rutgers")
    neb = output.find("Nebraska")
    iowa = output.find("Iowa")
    assert ucla < iu
    assert iu < nw
    assert nw < rut
    assert rut < neb
    assert neb < iowa
    
