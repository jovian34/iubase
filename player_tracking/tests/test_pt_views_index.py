import pytest
from django.urls import reverse
from datetime import date


this_year = date.today().year


@pytest.mark.django_db
def test_pt_index_renders(client):
    response = client.get(reverse("pt_index"))
    assert response.status_code == 200
    assert f"{this_year} Depth Chart" in str(response.content)
