from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.services.audio_detector import audio_detector
from app.services.image_detector import image_detector


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB, load ML models."""
    init_db()
    audio_detector.load_model()
    image_detector.load_model()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-Powered Deepfake Detection Toolkit",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for dashboard
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
async def dashboard():
    return FileResponse("static/index.html")


# --- Health Check ---

@app.get("/health", tags=["system"])
async def health():
    from app.models.schemas import HealthResponse

    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        models_loaded={
            "audio": audio_detector.is_loaded,
            "image": image_detector.is_loaded,
        },
    )


# --- Routers ---
from app.routers import audio, image, provenance, scans  # noqa: E402

app.include_router(audio.router)
app.include_router(image.router)
app.include_router(provenance.router)
app.include_router(scans.router)
