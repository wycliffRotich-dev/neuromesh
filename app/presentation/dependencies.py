from app.application.create_job_service import CreateJobService
from app.infrastructure.repositories.in_memory_job_repository import InMemoryJobRepository
from app.infrastructure.repositories.in_memory_node_repository import InMemoryNodeRepository

def get_create_job_service() -> CreateJobService:
    job_repo = InMemoryJobRepository()
    node_repo = InMemoryNodeRepository()
    
    return CreateJobService(
        job_repository=job_repo,
        node_repository=node_repo,
    )