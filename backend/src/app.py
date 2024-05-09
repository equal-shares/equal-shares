# Create the FastAPI application

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.config import init_config
from src.database import init_db
from src.logger import get_logger, init_loggers
from src.routers.admin import router as admin_router
from src.routers.form import router as form_router
from src.routers.report import router as report_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialize and Finalize the server"""

    # Initialize the server
    init_config()
    init_loggers()
    init_db()

    get_logger().info("The server started.")

    # The server will keep running until it is closed
    yield None

    # Finalize the server
    get_logger().info("The server closed.")


app = FastAPI(
    title="Equal Shares API",
    description="Equal Shares API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# root routes


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse("/docs")


@app.get("/health-check")
def health_check() -> dict:
    """Check if the server is running"""

    return {"status": "ok"}


# add routers
app.include_router(admin_router, prefix="/admin")
app.include_router(form_router, prefix="/form")
app.include_router(report_router, prefix="/report")
