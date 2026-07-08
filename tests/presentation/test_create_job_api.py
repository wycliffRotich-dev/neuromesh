from fastapi.testclient import TestClient

from app.presentation.api import app

client = TestClient(app)


def test_create_job_returns_201() -> None:
    """
    Creating a job through the API should return HTTP 201.
    """
    response = client.post(
        "/jobs",
        json={
            "cpu_cores": 4,
            "memory_mib": 4096,
            "vram_mib": 2048,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert "id" in body
    assert body["status"] == "SUBMITTED"
