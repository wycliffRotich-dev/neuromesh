from fastapi.testclient import TestClient

from app.presentation.api import app

client = TestClient(app)


def test_create_node_returns_201() -> None:
    """
    Creating a compute node should return HTTP 201.
    """
    response = client.post(
        "/nodes",
        json={
            "cpu_cores": 8,
            "memory_mib": 16384,
            "vram_mib": 4096,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert "id" in body
