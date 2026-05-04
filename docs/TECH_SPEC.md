# Technical Specification — DeepFakeGuard

> **Version:** 1.0
> **Date:** 2026-04-20
> **Status:** Draft

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                   Frontend                       │
│         HTML + Tailwind + Vanilla JS             │
└────────────────────┬────────────────────────────┘
                     │ HTTP
┌────────────────────▼────────────────────────────┐
│                FastAPI Server                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │  Audio    │ │  Image   │ │  C2PA Provenance │ │
│  │ Detector  │ │ Detector │ │     Viewer       │ │
│  └────┬─────┘ └────┬─────┘ └───────┬──────────┘ │
│       │            │               │             │
│  ┌────▼────────────▼───────────────▼──────────┐  │
│  │           AI Explainer (Claude API)         │  │
│  └───────────────────┬────────────────────────┘  │
│                      │                           │
│  ┌───────────────────▼────────────────────────┐  │
│  │              SQLite Database                │  │
│  │           (scan history, trends)            │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

## 2. Tech Stack

| Layer | Technology | Version | Why |
|-------|-----------|---------|-----|
| Language | Python | 3.11+ | ML/security standard |
| API | FastAPI | 0.110+ | Async, auto Swagger |
| Audio ML | PyTorch + Librosa | Latest | Spectrogram/MFCC features |
| Audio Model | Wav2Vec2 (HuggingFace) | — | SOTA voice anti-spoofing |
| Image ML | PyTorch + OpenCV | Latest | Face extraction, FFT |
| Image Model | ViT (HuggingFace) | — | ~92% deepfake image accuracy |
| AI Explainer | Claude API (Anthropic SDK) | Latest | Structured threat reports |
| Provenance | c2pa-python | Latest | C2PA Content Credentials |
| Database | SQLite | 3.x | Lightweight scan history |
| Frontend | HTML + Tailwind + Vanilla JS | — | No framework overhead |
| Testing | pytest + httpx | Latest | Async API testing |

## 3. Project Structure

```
deepfake/
├── docs/                          # Spec documents
│   ├── PRD.md
│   ├── TECH_SPEC.md
│   ├── API_SPEC.md
│   └── SPEC_INDEX.md
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Settings, env vars
│   ├── database.py                # SQLite connection, models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── audio.py               # Module 1: /api/v1/detect/audio
│   │   ├── image.py               # Module 2: /api/v1/detect/image
│   │   ├── provenance.py          # Module 4: /api/v1/provenance
│   │   └── scans.py               # Scan history: /api/v1/scans
│   ├── services/
│   │   ├── __init__.py
│   │   ├── audio_detector.py      # Audio feature extraction + model inference
│   │   ├── image_detector.py      # Image analysis + model inference
│   │   ├── explainer.py           # Claude API integration for explanations
│   │   └── provenance.py          # C2PA credential parsing
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic request/response models
│   └── utils/
│       ├── __init__.py
│       ├── audio_features.py      # Librosa feature extraction helpers
│       └── image_features.py      # OpenCV / FFT analysis helpers
├── ml/
│   ├── __init__.py
│   ├── download_models.py         # Script to download HF models
│   └── evaluate.py                # Model evaluation scripts
├── static/
│   ├── css/
│   ├── js/
│   └── index.html                 # Dashboard
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Shared fixtures
│   ├── test_audio.py
│   ├── test_image.py
│   ├── test_explainer.py
│   ├── test_provenance.py
│   └── test_api.py
├── requirements.txt
├── .env.example
├── .gitignore
├── CLAUDE.md
├── PROPOSAL.md
└── README.md
```

## 4. Data Models

### 4.1 Audio Detection Request

```python
class AudioDetectionRequest:
    file: UploadFile  # .wav, .mp3, .flac
```

### 4.2 Image Detection Request

```python
class ImageDetectionRequest:
    file: UploadFile  # .jpg, .png, .webp
```

### 4.3 Detection Response (shared structure)

```python
class DetectionResponse:
    id: str                      # UUID
    verdict: str                 # "real" | "synthetic" | "manipulated"
    confidence: float            # 0.0 - 1.0
    media_type: str              # "audio" | "image"
    analysis: dict               # Module-specific artifacts
    c2pa_credentials: dict|None  # Provenance data (if checked)
    ai_explanation: str          # Plain-English explanation
    severity: str                # "low" | "medium" | "high" | "critical"
    action: str                  # Recommended action
    mitre_atlas: str             # e.g., "AML.T0048"
    timestamp: str               # ISO 8601
```

### 4.4 Audio Analysis Details

```python
class AudioAnalysis:
    spectral_artifacts: bool
    pitch_consistency: float     # 0.0 - 1.0
    breathing_patterns: str      # "natural" | "absent" | "irregular"
    background_noise: str        # description
    codec_artifacts: str         # description
    duration_seconds: float
```

### 4.5 Image Analysis Details

```python
class ImageAnalysis:
    gan_artifacts: bool
    frequency_anomalies: str     # description
    facial_symmetry: float       # 0.0 - 1.0
    lighting_consistency: float  # 0.0 - 1.0
    metadata_integrity: str      # "clean" | "exif_stripped" | "inconsistent"
    face_detected: bool
```

### 4.6 C2PA Provenance Response

```python
class ProvenanceResponse:
    has_credentials: bool
    status: str                  # "verified" | "none" | "tampered"
    manifest: dict|None          # Full C2PA manifest data
    creator_tool: str|None
    creation_date: str|None
    edit_history: list|None
    ai_generated_flag: bool|None
```

### 4.7 Scan History Record (SQLite)

```sql
CREATE TABLE scans (
    id TEXT PRIMARY KEY,
    media_type TEXT NOT NULL,
    verdict TEXT NOT NULL,
    confidence REAL NOT NULL,
    severity TEXT NOT NULL,
    filename TEXT,
    ai_explanation TEXT,
    mitre_atlas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 5. Environment Configuration

```env
# .env.example
ANTHROPIC_API_KEY=sk-ant-...
MODEL_AUDIO=MelodyMachine/Deepfake-audio-detection-V2
MODEL_IMAGE=prithivMLmods/Deep-Fake-Detector-v2-Model
DATABASE_URL=sqlite:///./deepfakeguard.db
MAX_AUDIO_SIZE_MB=50
MAX_IMAGE_SIZE_MB=20
LOG_LEVEL=INFO
```

## 6. ML Model Strategy

### 6.1 Audio Model

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Base model | Pre-trained from HuggingFace | Avoid training from scratch; competitive results |
| Primary candidate | `MelodyMachine/Deepfake-audio-detection-V2` | Fine-tuned Wav2Vec2 for deepfake audio |
| Evaluation dataset | ASVspoof 5 (Track 1) | Gold-standard benchmark |
| Supplementary test | MLAAD v9 samples | Multilingual generalization |
| Metrics | EER, precision, recall, minDCF | Standard anti-spoofing metrics |

### 6.2 Image Model

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Base model | Pre-trained ViT from HuggingFace | ~92% accuracy reported |
| Primary candidate | `prithivMLmods/Deep-Fake-Detector-v2-Model` | ViT-based, well-documented |
| Evaluation dataset | DF40 test set | 40 deepfake techniques |
| Cross-generator test | Images from unseen generators | Test generalization |
| Metrics | AUC, accuracy, precision/recall per forgery type | Standard CV metrics |

### 6.3 Model Storage

Models will be downloaded to a local `ml/models/` directory (gitignored). Download handled by `ml/download_models.py`.

## 7. Error Handling Strategy

| Error | Response |
|-------|----------|
| Invalid file type | 415 Unsupported Media Type |
| File too large | 413 Payload Too Large |
| No file provided | 400 Bad Request |
| Model not loaded | 503 Service Unavailable |
| Claude API failure | 502 Bad Gateway (return detection results without explanation) |
| C2PA parse failure | Return detection results with `c2pa_credentials: null` |

## 8. Testing Strategy

| Type | Scope | Tool |
|------|-------|------|
| Unit | Feature extraction, model inference | pytest |
| Integration | Full API endpoints | httpx + FastAPI TestClient |
| Evaluation | Model accuracy on benchmarks | Custom scripts |
| Smoke | End-to-end upload → detect → explain | pytest |

## 9. Build Order (Module Dependencies)

```
Module 1 (Audio) ──┐
                    ├──▶ Module 3 (Explainer) ──▶ Module 5 (Dashboard)
Module 2 (Image) ──┤
                    ├──▶ Module 4 (C2PA) ────────▶ Module 5 (Dashboard)
                    │
              Shared: FastAPI skeleton, config, DB
```

Modules 1, 2, and 4 can be developed in parallel. Module 3 depends on 1 and 2 being done. Module 5 integrates everything.
