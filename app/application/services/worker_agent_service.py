from app.domain.entities.job import Job
from app.domain.entities.worker import Worker


class WorkerAgentService:

    def assign(
        self,
        worker: Worker,
        job: Job,
    ) -> None:
        worker.accept(job)

    def start(
        self,
        worker: Worker,
    ) -> None:
        worker.start()

    def complete(
        self,
        worker: Worker,
    ) -> None:
        worker.complete()

    def fail(
        self,
        worker: Worker,
    ) -> None:
        worker.fail()
