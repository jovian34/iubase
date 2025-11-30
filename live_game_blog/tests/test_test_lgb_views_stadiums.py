import pytest
from django import urls


def test_stadium_page_renders(client):
    response = client.get(urls.reverse("stadiums"))
    assert response.status_code == 200