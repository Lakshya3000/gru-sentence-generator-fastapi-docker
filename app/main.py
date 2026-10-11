from contextlib import asynccontextmanager
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import APP_NAME, APP_VERSION
from app.services.model_service import ModelService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    service = ModelService()
    service.load()  # Fail fast if required model artifacts are missing or invalid.
    app.state.model_service = service
    yield
    app.state.model_service = None


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="REST API for generating text with a trained GRU model.",
    lifespan=lifespan,
)
app.include_router(router)
STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
