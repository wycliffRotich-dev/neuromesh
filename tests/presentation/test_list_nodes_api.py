from fastapi.testclient import TestClient

from app.presentation.api import app

client = TestClient(app)


def test_list_nodes_returns_200() -> None:
    """
    Listing compute nodes should return HTTP 200.
    """
    response = client.get("/nodes")

    assert response.status_code == 200

    body = response.json()

    assert "nodes" in body
    assert isinstance(body["nodes"], list)