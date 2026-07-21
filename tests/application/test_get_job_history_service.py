from app.application.services.get_job_history_service import (
    GetJobHistoryService,
)
from app.application.services.record_job_events_service import (
    RecordJobEventsService,
)
from app.infrastructure.repositories.in_memory_event_repository import (
    InMemoryEventRepository,
)


def test_returns_job_history() -> None:
    repository = InMemoryEventRepository()

    recorder = RecordJobEventsService(
        event_repository=repository,
    )

    recorder.record(
        aggregate_id="job-123",
        aggregate_type="Job",
        event_type="JobCreated",
    )

    recorder.record(
        aggregate_id="job-123",
        aggregate_type="Job",
        event_type="JobQueued",
    )

    recorder.record(
        aggregate_id="job-123",
        aggregate_type="Job",
        event_type="JobScheduled",
    )

    service = GetJobHistoryService(
        event_repository=repository,
    )

    events = service.execute(
        aggregate_id="job-123",
    )

    assert len(events) == 3

    assert events[0].event_type == "JobCreated"
    assert events[1].event_type == "JobQueued"
    assert events[2].event_type == "JobScheduled"
