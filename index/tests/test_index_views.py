import pytest


def test_index_renders(client):
    response = client.get("/index/")
    assert response.status_code == 200