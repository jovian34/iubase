import pytest
from django import shortcuts, urls

from conference import year


@pytest.mark.django_db
def test_standings_page_for_prior_year_renders(client):
    response = client.get(urls.reverse("standings", args=[year.get_spring_year()-1]))
    assert response.status_code == 200