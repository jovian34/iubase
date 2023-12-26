import pytest


def test_index_renders(client):
    response = client.get("/live_game_blog/")
    assert response.status_code == 200