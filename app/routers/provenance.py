"""C2PA Content Credentials endpoint."""

from fastapi import APIRouter, File, UploadFile

from app.models.schemas import ErrorResponse, ProvenanceResponse
from app.services.provenance import check_provenance

router = APIRouter(prefix="/api/v1", tags=["provenance"])

ALLOWED = {".jpg", ".jpeg", ".png", ".webp", ".wav", ".mp3", ".flac", ".mp4"}
MAX_BYTES = 50 * 1024 * 1024  # 50 MB


@router.post(
    "/provenance",
    response_model=ProvenanceResponse,
    responses={
        400: {"model": ErrorResponse},
        413: {"model": ErrorResponse},
    },
)
async def check_media_provenance(file: UploadFile = File(...)):
    """Check if a media file has C2PA Content Credentials."""

    if not file.filename:
        return ProvenanceResponse(
            has_credentials=False, status="none", manifest=None,
            eu_ai_act_note="No filename provided.",
        )

    from pathlib import Path
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED:
        return ProvenanceResponse(
            has_credentials=False, status="none", manifest=None,
            eu_ai_act_note=f"File type '{ext}' is not supported for provenance checking.",
        )

    file_bytes = await file.read()

    if len(file_bytes) > MAX_BYTES:
        return ProvenanceResponse(
            has_credentials=False, status="none", manifest=None,
            eu_ai_act_note=f"File exceeds maximum size of {MAX_BYTES // (1024*1024)}MB.",
        )

    return check_provenance(file_bytes, file.filename)
