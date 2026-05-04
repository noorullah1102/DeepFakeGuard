"""Tests for Module 2 — Image Deepfake Detector."""

import io

import numpy as np
import pytest
from PIL import Image


def _make_jpeg(width: int = 200, height: int = 200) -> bytes:
    """Generate a minimal JPEG image in memory."""
    img = Image.fromarray(np.random.randint(0, 255, (height, width, 3), dtype=np.uint8))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf.read()


@pytest.fixture
def jpeg_bytes():
    return _make_jpeg()


@pytest.mark.asyncio
async def test_image_detect_real_jpeg(client, jpeg_bytes):
    """Should accept a JPEG file and return a detection result."""
    response = await client.post(
        "/api/v1/detect/image",
        files={"file": ("test.jpg", jpeg_bytes, "image/jpeg")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["media_type"] == "image"
    assert data["verdict"] in ("real", "manipulated")
    assert 0.0 <= data["confidence"] <= 1.0
    assert "analysis" in data
    assert "ai_explanation" in data
    assert data["severity"] in ("low", "medium", "high", "critical")
    assert data["mitre_atlas"] == "AML.T0048.002"


@pytest.mark.asyncio
async def test_image_reject_bad_extension(client, jpeg_bytes):
    """Should reject non-image file types."""
    response = await client.post(
        "/api/v1/detect/image",
        files={"file": ("test.exe", jpeg_bytes, "application/octet-stream")},
    )
    assert response.status_code == 415
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "UNSUPPORTED_MEDIA_TYPE"


@pytest.mark.asyncio
async def test_image_analysis_fields(client, jpeg_bytes):
    """Image analysis should contain expected fields."""
    response = await client.post(
        "/api/v1/detect/image",
        files={"file": ("test.jpg", jpeg_bytes, "image/jpeg")},
    )
    data = response.json()
    analysis = data["analysis"]
    assert "gan_artifacts" in analysis
    assert "frequency_anomalies" in analysis
    assert "lighting_consistency" in analysis
    assert "metadata_integrity" in analysis
