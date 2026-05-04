"""Scan history endpoints."""

from fastapi import APIRouter, Path, Query

from app.database import get_scan_by_id, get_scans
from app.models.schemas import ErrorResponse, ScanListResponse

router = APIRouter(prefix="/api/v1/scans", tags=["scans"])


@router.get("", response_model=ScanListResponse)
async def list_scans(
    media_type: str | None = Query(None, description="Filter: audio or image"),
    verdict: str | None = Query(None, description="Filter: real, synthetic, manipulated"),
    severity: str | None = Query(None, description="Filter: low, medium, high, critical"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Retrieve scan history with optional filtering and pagination."""
    scans, total = get_scans(
        media_type=media_type,
        verdict=verdict,
        severity=severity,
        limit=limit,
        offset=offset,
    )
    return ScanListResponse(total=total, limit=limit, offset=offset, scans=scans)


@router.get(
    "/{scan_id}",
    responses={404: {"model": ErrorResponse}},
)
async def get_scan(
    scan_id: str = Path(..., description="Scan UUID"),
):
    """Retrieve a single scan by ID."""
    scan = get_scan_by_id(scan_id)
    if not scan:
        return ErrorResponse(error={"code": "NOT_FOUND", "message": f"Scan '{scan_id}' not found"})
    return dict(scan)
