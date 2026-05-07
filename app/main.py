import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.config import get_settings
from app.routers import inference, ingestion
from app.utils.logging_config import setup_logging

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
     # Configure logging FIRST
    setup_logging()

    # Startup log (now goes to file)
    logger.info("Starting AI Powered Academic Support System RAG Service")

    yield  # Application runs here

    # Shutdown log
    logger.info("Shutting down AI Powered Academic Support System RAG Service")


app = FastAPI(
    title="AI RAG Service",
    version="1.0.0",
    lifespan=lifespan,
    debug=True
)

# Include routers
app.include_router(ingestion.router, prefix="/api/v1", tags=['ingestion'])
app.include_router(inference.router, prefix="/api/v1", tags=['inference'])