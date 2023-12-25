import pytest
from django.urls import reverse


def test_index_renders(client):
    response = client.get(reverse("index"))
    assert response.status_code == 200