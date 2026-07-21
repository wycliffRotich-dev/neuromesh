from fastapi.testclient import TestClient

from app.presentation.api import app

client = TestClient(app)


def test_get_job_history_returns_200() -> None:
    response = client.get(
        "/jobs/job-123/history",
    )

    assert response.status_code == 200
