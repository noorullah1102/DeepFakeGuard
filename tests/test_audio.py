"""Tests for Module 1 — Audio Deepfake Detector."""

import io

import numpy as np
import pytest
import soundfile as sf


def _make_wav(duration_sec: float = 1.0, sr: int = 16000) -> bytes:
    """Generate a minimal valid WAV file in memory."""
    t = np.linspace(0, duration_sec, int(sr * duration_sec), dtype=np.float32)
    waveform = (0.3 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
    buf = io.BytesIO()
    sf.write(buf, waveform, sr, format="WAV")
    buf.seek(0)
    return buf.read()


@pytest.fixture
def wav_bytes():
    return _make_wav(duration_sec=0.5)


@pytest.mark.asyncio
async def test_audio_detect_real_wav(client, wav_bytes):
    """Should accept a WAV file and return a detection result."""
    response = await client.post(
        "/api/v1/detect/audio",
        files={"file": ("test.wav", wav_bytes, "audio/wav")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["media_type"] == "audio"
    assert data["verdict"] in ("real", "synthetic")
    assert 0.0 <= data["confidence"] <= 1.0
    assert "analysis" in data
    assert "ai_explanation" in data
    assert data["severity"] in ("low", "medium", "high", "critical")
    assert data["mitre_atlas"] == "AML.T0048"


@pytest.mark.asyncio
async def test_audio_reject_bad_extension(client, wav_bytes):
    """Should reject non-audio file types."""
    response = await client.post(
        "/api/v1/detect/audio",
        files={"file": ("test.txt", wav_bytes, "text/plain")},
    )
    assert response.status_code == 415
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "UNSUPPORTED_MEDIA_TYPE"


@pytest.mark.asyncio
async def test_audio_analysis_fields(client, wav_bytes):
    """Audio analysis should contain expected fields."""
    response = await client.post(
        "/api/v1/detect/audio",
        files={"file": ("test.wav", wav_bytes, "audio/wav")},
    )
    data = response.json()
    analysis = data["analysis"]
    assert "spectral_artifacts" in analysis
    assert "pitch_consistency" in analysis
    assert "breathing_patterns" in analysis
    assert "duration_seconds" in analysis
