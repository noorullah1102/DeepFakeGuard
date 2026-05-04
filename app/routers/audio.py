"""Audio deepfake detection endpoint."""

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from app.database import insert_scan
from app.services.audio_detector import audio_detector
from app.utils.audio_features import validate_audio_file

router = APIRouter(prefix="/api/v1/detect", tags=["audio"])

MAX_AUDIO_BYTES = 50 * 1024 * 1024  # 50 MB


@router.post("/audio")
async def detect_audio(file: UploadFile = File(...)):
    """Upload an audio file (.wav, .mp3, .flac) and get a deepfake detection result."""

    if not file.filename:
        return JSONResponse(status_code=400, content={"error": {"code": "INVALID_FILENAME", "message": "Filename is required"}})

    try:
        validate_audio_file(file.filename)
    except ValueError as e:
        return JSONResponse(status_code=415, content={"error": {"code": "UNSUPPORTED_MEDIA_TYPE", "message": str(e)}})

    audio_bytes = await file.read()

    if len(audio_bytes) > MAX_AUDIO_BYTES:
        return JSONResponse(status_code=413, content={"error": {"code": "FILE_TOO_LARGE", "message": f"File exceeds maximum size of {MAX_AUDIO_BYTES // (1024*1024)}MB"}})

    result = audio_detector.detect(audio_bytes, filename=file.filename)

    from app.services.explainer import generate_explanation
    explanation, action = generate_explanation(result)
    result["ai_explanation"] = explanation
    result["action"] = action

    insert_scan(result)

    return result
