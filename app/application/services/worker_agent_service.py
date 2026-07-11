from app.domain.workers.worker_agent import WorkerAgent

from app.domain.entities.job import Job


class WorkerAgentService:

    def assign(
        self,
        worker: WorkerAgent,
        job: Job,
    ) -> None:

        worker.accept_job(job)


    def start(
        self,
        worker: WorkerAgent,
    ) -> None:

        worker.execute()


    def complete(
        self,
        worker: WorkerAgent,
    ) -> None:

        worker.complete()


    def fail(
        self,
        worker: WorkerAgent,
    ) -> None:

        worker.fail()
