import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import chat, crowd, queue, routing, recommendation
from app.core.config import settings
from app.models.schemas import StandardResponse

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    # Allow common local frontend dev ports
    origins = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} completed in {process_time:.4f}s with status {response.status_code}")
        return response

    # Include API routers
    app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
    app.include_router(crowd.router, prefix="/api/v1/crowd", tags=["crowd"])
    app.include_router(queue.router, prefix="/api/v1/queue", tags=["queue"])
    app.include_router(routing.router, prefix="/api/v1/routing", tags=["routing"])
    app.include_router(recommendation.router, prefix="/api/v1/recommendation", tags=["recommendation"])

    @app.get("/api/v1/health", response_model=StandardResponse[dict], tags=["system"])
    async def health_check():
        return StandardResponse(status="success", data={"environment": settings.ENVIRONMENT, "status": "ok"})

    return app

app = create_app()
