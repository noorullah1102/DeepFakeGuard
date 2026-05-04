from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


# --- Audio Analysis ---

class AudioAnalysis(BaseModel):
    spectral_artifacts: bool
    pitch_consistency: float = Field(ge=0.0, le=1.0)
    breathing_patterns: str  # "natural" | "absent" | "irregular"
    background_noise: str
    codec_artifacts: str
    duration_seconds: float


# --- Image Analysis ---

class ImageAnalysis(BaseModel):
    gan_artifacts: bool
    frequency_anomalies: str
    facial_symmetry: float = Field(ge=0.0, le=1.0)
    lighting_consistency: float = Field(ge=0.0, le=1.0)
    metadata_integrity: str  # "clean" | "exif_stripped" | "inconsistent"
    face_detected: bool


# --- C2PA Provenance ---

class C2PAEditEntry(BaseModel):
    action: str
    tool: str | None = None
    timestamp: str | None = None


class C2PAManifest(BaseModel):
    creator_tool: str | None = None
    creation_date: str | None = None
    edit_history: list[C2PAEditEntry] | None = None
    ai_generated_flag: bool | None = None


class ProvenanceResponse(BaseModel):
    has_credentials: bool
    status: Literal["verified", "none", "tampered"]
    manifest: C2PAManifest | None = None
    eu_ai_act_note: str = ""


# --- Shared Detection Response ---

class DetectionResponse(BaseModel):
    id: str
    verdict: Literal["real", "synthetic", "manipulated"]
    confidence: float = Field(ge=0.0, le=1.0)
    media_type: Literal["audio", "image"]
    analysis: AudioAnalysis | ImageAnalysis
    c2pa_credentials: ProvenanceResponse | None = None
    ai_explanation: str = ""
    severity: Literal["low", "medium", "high", "critical"]
    action: str = ""
    mitre_atlas: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# --- Scan History ---

class ScanSummary(BaseModel):
    id: str
    media_type: str
    verdict: str
    confidence: float
    severity: str
    filename: str | None = None
    timestamp: str


class ScanListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    scans: list[ScanSummary]


# --- Error ---

class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail


# --- Health ---

class HealthResponse(BaseModel):
    status: str
    version: str
    models_loaded: dict[str, bool]
