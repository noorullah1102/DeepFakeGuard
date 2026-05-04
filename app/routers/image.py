"""Image deepfake detection endpoint."""

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from app.database import insert_scan
from app.services.image_detector import image_detector
from app.utils.image_features import validate_image_file

router = APIRouter(prefix="/api/v1/detect", tags=["image"])

MAX_IMAGE_BYTES = 20 * 1024 * 1024  # 20 MB


@router.post("/image")
async def detect_image(file: UploadFile = File(...)):
    """Upload an image (.jpg, .png, .webp) and get a deepfake detection result."""

    if not file.filename:
        return JSONResponse(status_code=400, content={"error": {"code": "INVALID_FILENAME", "message": "Filename is required"}})

    try:
        validate_image_file(file.filename)
    except ValueError as e:
        return JSONResponse(status_code=415, content={"error": {"code": "UNSUPPORTED_MEDIA_TYPE", "message": str(e)}})

    image_bytes = await file.read()

    if len(image_bytes) > MAX_IMAGE_BYTES:
        return JSONResponse(status_code=413, content={"error": {"code": "FILE_TOO_LARGE", "message": f"File exceeds maximum size of {MAX_IMAGE_BYTES // (1024*1024)}MB"}})

    result = image_detector.detect(image_bytes, filename=file.filename)

    from app.services.explainer import generate_explanation
    explanation, action = generate_explanation(result)
    result["ai_explanation"] = explanation
    result["action"] = action

    insert_scan(result)

    return result
