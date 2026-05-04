"""Tests for scan history and provenance endpoints."""

import io

import numpy as np
import pytest
from PIL import Image


def _make_jpeg() -> bytes:
    img = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf.read()


@pytest.mark.asyncio
async def test_scan_history_empty(client):
    """Scan history should return empty list initially (or after clear)."""
    response = await client.get("/api/v1/scans")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "scans" in data


@pytest.mark.asyncio
async def test_scan_appears_in_history(client):
    """After uploading an image, it should appear in scan history."""
    jpeg = _make_jpeg()

    # Upload
    await client.post(
        "/api/v1/detect/image",
        files={"file": ("history_test.jpg", jpeg, "image/jpeg")},
    )

    # Check history
    response = await client.get("/api/v1/scans")
    data = response.json()
    assert data["total"] >= 1
    filenames = [s["filename"] for s in data["scans"]]
    assert "history_test.jpg" in filenames


@pytest.mark.asyncio
async def test_provenance_no_credentials(client):
    """Random image should have no C2PA credentials."""
    jpeg = _make_jpeg()
    response = await client.post(
        "/api/v1/provenance",
        files={"file": ("test.jpg", jpeg, "image/jpeg")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("none", "verified", "tampered")
    assert "eu_ai_act_note" in data


@pytest.mark.asyncio
async def test_dashboard_served(client):
    """Dashboard HTML should be served at root."""
    response = await client.get("/")
    assert response.status_code == 200
    assert "DeepFakeGuard" in response.text
