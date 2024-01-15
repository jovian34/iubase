import pytest
from django.urls import reverse


def test_index(client):
    response = client.get(reverse("players"))
    assert response.status_code == 200
