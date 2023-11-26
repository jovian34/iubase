import pytest


def test_index_redirect(client):
    response = client.get("")
    assert response.status_code == 302