import pytest
from django import urls


@pytest.mark.django_db
def test_index_renders(client):
    response = client.get(urls.reverse("index"))
    assert response.status_code == 200
    assert "Live Game Blogs" in str(response.content)
