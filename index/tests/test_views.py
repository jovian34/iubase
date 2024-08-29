import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_index_renders(client):
    response = client.get(reverse("index"))
    assert response.status_code == 200
    assert "Live Game Blogs" in str(response.content)
