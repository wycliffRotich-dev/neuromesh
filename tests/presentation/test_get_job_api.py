from fastapi.testclient import TestClient

from app.presentation.api import app

client = TestClient(app)


def test_get_existing_job_returns_200() -> None:
    """
    Retrieving an existing job should return HTTP 200.
    """
    create_response = client.post(
        "/jobs",
        json={
            "cpu_cores": 4,
            "memory_mib": 4096,
            "vram_mib": 2048,
        },
    )

    job_id = create_response.json()["id"]

    response = client.get(
        f"/jobs/{job_id}",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == job_id
    assert body["status"] == "SUBMITTED"
    assert body["cpu_cores"] == 4
    assert body["memory_mib"] == 4096
    assert body["vram_mib"] == 2048


def test_get_unknown_job_returns_404() -> None:
    """
    Retrieving a non-existent job should return HTTP 404.
    """
    response = client.get(
        "/jobs/00000000-0000-0000-0000-000000000000",
    )

    assert response.status_code == 404