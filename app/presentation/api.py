from fastapi import FastAPI

from app.presentation.routers.jobs import router as jobs_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(jobs_router)

    return app