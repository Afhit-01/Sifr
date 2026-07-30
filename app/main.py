import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.logger import get_logger
from app.routes import health, items

settings = get_settings()
logger = get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="A production-style FastAPI service demonstrating core DevOps practices.",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── Middleware: request timing & structured access log ──────────────────
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "method=%s path=%s status=%d duration=%.1fms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response

    # ── Global exception handler ────────────────────────────────────────────
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    # ── Routers ─────────────────────────────────────────────────────────────
    app.include_router(health.router)
    app.include_router(items.router)

    @app.on_event("startup")
    async def startup_event():
        logger.info(
            "Starting %s v%s in [%s] mode",
            settings.app_name,
            settings.app_version,
            settings.environment,
        )

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down %s", settings.app_name)

    return app


app = create_app()
