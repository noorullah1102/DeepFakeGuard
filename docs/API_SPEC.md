# API Specification — DeepFakeGuard

> **Version:** 1.0
> **Date:** 2026-04-20
> **Status:** Draft
> **Base URL:** `http://localhost:8000`

## 1. General

### 1.1 Content Types

- **Request:** `multipart/form-data` (file uploads)
- **Response:** `application/json`

### 1.2 Common Response Fields

All detection responses include:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | UUID for this scan |
| `verdict` | string | `"real"`, `"synthetic"`, or `"manipulated"` |
| `confidence` | float | 0.0 – 1.0 |
| `media_type` | string | `"audio"` or `"image"` |
| `analysis` | object | Module-specific artifact details |
| `c2pa_credentials` | object\|null | Provenance data if checked |
| `ai_explanation` | string | Plain-English explanation |
| `severity` | string | `"low"`, `"medium"`, `"high"`, `"critical"` |
| `action` | string | Recommended next step |
| `mitre_atlas` | string | MITRE ATLAS technique ID |
| `timestamp` | string | ISO 8601 datetime |

### 1.3 Error Response Format

```json
{
  "error": {
    "code": "UNSUPPORTED_MEDIA_TYPE",
    "message": "File type '.txt' is not supported. Accepted: .wav, .mp3, .flac"
  }
}
```

### 1.4 Error Codes

| HTTP Status | Error Code | When |
|-------------|-----------|------|
| 400 | `MISSING_FILE` | No file in request |
| 400 | `INVALID_FILENAME` | Filename missing or empty |
| 413 | `FILE_TOO_LARGE` | Exceeds max size |
| 415 | `UNSUPPORTED_MEDIA_TYPE` | Wrong file extension |
| 503 | `MODEL_NOT_LOADED` | ML model not available |
| 502 | `EXPLAINER_UNAVAILABLE` | Claude API failed |

---

## 2. Endpoints

### 2.1 Health Check

```
GET /health
```

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "models_loaded": {
    "audio": true,
    "image": true
  }
}
```

---

### 2.2 Detect Audio

```
POST /api/v1/detect/audio
```

**Request:** `multipart/form-data`

| Field | Type | Required | Accepted |
|-------|------|----------|----------|
| `file` | file | Yes | `.wav`, `.mp3`, `.flac` |

**Response (200):**

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "verdict": "synthetic",
  "confidence": 0.91,
  "media_type": "audio",
  "analysis": {
    "spectral_artifacts": true,
    "pitch_consistency": 0.43,
    "breathing_patterns": "absent",
    "background_noise": "unnaturally_uniform",
    "codec_artifacts": "consistent_with_tts",
    "duration_seconds": 47.2
  },
  "c2pa_credentials": null,
  "ai_explanation": "This audio shows multiple indicators of AI generation...",
  "severity": "high",
  "action": "Do not act on any instructions from this call. Verify the speaker's identity through a known, separate channel.",
  "mitre_atlas": "AML.T0048",
  "timestamp": "2026-04-20T14:30:00Z"
}
```

| `verdict` | `severity` | Meaning |
|-----------|-----------|---------|
| `"real"` | `"low"` | No synthetic artifacts detected |
| `"synthetic"` | `"high"` or `"critical"` | AI-generated audio detected |

---

### 2.3 Detect Image

```
POST /api/v1/detect/image
```

**Request:** `multipart/form-data`

| Field | Type | Required | Accepted |
|-------|------|----------|----------|
| `file` | file | Yes | `.jpg`, `.png`, `.webp` |

**Response (200):**

```json
{
  "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "verdict": "manipulated",
  "confidence": 0.87,
  "media_type": "image",
  "analysis": {
    "gan_artifacts": true,
    "frequency_anomalies": "high_frequency_grid_pattern",
    "facial_symmetry": 0.98,
    "lighting_consistency": 0.62,
    "metadata_integrity": "exif_stripped",
    "face_detected": true
  },
  "c2pa_credentials": null,
  "ai_explanation": "This headshot shows signs of AI generation...",
  "severity": "high",
  "action": "Do not use this image for identity verification. Request a live video verification.",
  "mitre_atlas": "AML.T0048.002",
  "timestamp": "2026-04-20T14:32:00Z"
}
```

---

### 2.4 Check Provenance

```
POST /api/v1/provenance
```

**Request:** `multipart/form-data`

| Field | Type | Required | Accepted |
|-------|------|----------|----------|
| `file` | file | Yes | `.jpg`, `.png`, `.webp`, `.wav`, `.mp3`, `.mp4` |

**Response — Credentials Present (200):**

```json
{
  "has_credentials": true,
  "status": "verified",
  "manifest": {
    "creator_tool": "DALL-E 3",
    "creation_date": "2026-03-15T10:22:00Z",
    "edit_history": [
      {
        "action": "created",
        "tool": "DALL-E 3",
        "timestamp": "2026-03-15T10:22:00Z"
      }
    ],
    "ai_generated_flag": true
  },
  "eu_ai_act_note": "This media carries C2PA Content Credentials indicating AI generation. Under EU AI Act Article 50, this disclosure meets transparency obligations effective August 2026."
}
```

**Response — No Credentials (200):**

```json
{
  "has_credentials": false,
  "status": "none",
  "manifest": null,
  "eu_ai_act_note": "No C2PA Content Credentials found. This media cannot be verified for provenance. Under EU AI Act Article 50, AI-generated media should carry machine-readable labels by August 2026."
}
```

**Response — Tampered (200):**

```json
{
  "has_credentials": false,
  "status": "tampered",
  "manifest": null,
  "eu_ai_act_note": "C2PA Content Credentials are present but fail validation. The credential chain may have been modified or corrupted."
}
```

---

### 2.5 List Scan History

```
GET /api/v1/scans
```

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `media_type` | string | all | Filter: `"audio"` or `"image"` |
| `verdict` | string | all | Filter: `"real"`, `"synthetic"`, `"manipulated"` |
| `severity` | string | all | Filter: `"low"`, `"medium"`, `"high"`, `"critical"` |
| `limit` | int | 50 | Max results (1-100) |
| `offset` | int | 0 | Pagination offset |

**Response (200):**

```json
{
  "total": 142,
  "limit": 50,
  "offset": 0,
  "scans": [
    {
      "id": "a1b2c3d4-...",
      "media_type": "audio",
      "verdict": "synthetic",
      "confidence": 0.91,
      "severity": "high",
      "filename": "ceo_urgent_call.wav",
      "timestamp": "2026-04-20T14:30:00Z"
    }
  ]
}
```

---

### 2.6 Get Single Scan

```
GET /api/v1/scans/{scan_id}
```

**Response (200):** Full `DetectionResponse` object (same as detection response).

**Response (404):**

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Scan 'abc123' not found"
  }
}
```

---

## 3. Severity Scoring Logic

Severity is computed from model confidence + artifact count + metadata signals:

```
if confidence >= 0.85 AND artifact_count >= 3:
    severity = "critical"
elif confidence >= 0.70 AND artifact_count >= 2:
    severity = "high"
elif confidence >= 0.50:
    severity = "medium"
else:
    severity = "low"
```

Adjustments:
- `exif_stripped` on images: +1 severity level
- `c2pa_credentials.status == "tampered"`: +1 severity level
- `breathing_patterns == "absent"` on audio: +1 severity level

---

## 4. MITRE ATLAS Mapping

| Detection | MITRE ATLAS ID |
|-----------|---------------|
| Audio deepfake | `AML.T0048` |
| Image deepfake | `AML.T0048.002` |
| Synthetic identity | `AML.T0048.002` |
| Voice cloning | `AML.T0048.001` |
