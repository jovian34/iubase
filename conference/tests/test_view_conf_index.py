import pytest

from django import shortcuts, urls
from conference.logic import year


@pytest.mark.django_db
def test_conf_index_renders(client):
    response = client.get(urls.reverse("conf_index"))
    assert response.status_code == 200
    assert "Conference Apps" in response.content.decode()
    assert f"{year.get_spring_year()} B1G Conference Schedule" in response.content.decode()
    assert f"conference/schedule/{year.get_spring_year()}/" in response.content.decode()
    assert f"{year.get_spring_year()} B1G Conference Members" in response.content.decode()
    assert f"conference/members/B1G/{year.get_spring_year()}/" in response.content.decode()