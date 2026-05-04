# CLAUDE.md — DeepFakeGuard

## Project Overview

DeepFakeGuard is an open-source AI-powered deepfake detection toolkit. It detects AI-generated voices and manipulated images via a REST API, explains findings in plain English using Claude, and checks media provenance via C2PA Content Credentials.

## Tech Stack

- **Language:** Python 3.12
- **API:** FastAPI with auto-generated Swagger docs
- **Audio ML:** PyTorch + Librosa + Wav2Vec2-Large-XLSR (HuggingFace: `garystafford/wav2vec2-deepfake-voice-detector`) — trained on ElevenLabs, Amazon Polly, Kokoro, Speechify, and other modern TTS engines
- **Image ML (dual-model ensemble):**
  - **CommunityForensics ViT** (`buildborderless/CommunityForensics-DeepfakeDet-ViT`) — ViT-Base, 384x384 input, single-logit sigmoid output. Requires manual preprocessing (resize to 384x384 + normalize) because the model's `AutoImageProcessor` has a broken resize-to-440-then-crop pipeline. Labels: `{0: real, 1: fake}`.
  - **prithivMLmods SigLIP** (`prithivMLmods/deepfake-detector-model-v1`) — SigLIP architecture, works with `AutoImageProcessor` out of the box. Labels: `{0: 'Fake', 1: 'Real'}`.
- **AI Explainer:** Claude API via Anthropic SDK (model: `claude-haiku-4-5-20251001`) with fallback templates
- **Provenance:** c2pa-python (optional dependency)
- **Database:** SQLite for scan history
- **Frontend:** HTML + Tailwind + vanilla JS (dark theme dashboard)
- **Testing:** pytest + pytest-asyncio + httpx

## Project Structure

```
app/
├── main.py                 # FastAPI entry point, lifespan (DB init + model loading)
├── config.py               # Pydantic settings from .env (model_image, model_image_ensemble)
├── database.py             # SQLite CRUD for scan history
├── models/schemas.py       # All Pydantic request/response models
├── routers/
│   ├── audio.py            # POST /api/v1/detect/audio
│   ├── image.py            # POST /api/v1/detect/image
│   ├── provenance.py       # POST /api/v1/provenance
│   └── scans.py            # GET /api/v1/scans, GET /api/v1/scans/{id}
├── services/
│   ├── audio_detector.py   # Audio feature extraction + Wav2Vec2 inference
│   ├── image_detector.py   # Dual-model ensemble (CommunityForensics + prithivMLmods)
│   ├── explainer.py        # Claude API integration + fallback templates
│   └── provenance.py       # C2PA manifest parsing
└── utils/
    ├── audio_features.py   # Librosa: MFCCs, spectrograms, pitch, breathing detection
    └── image_features.py   # OpenCV: FFT, GAN artifacts, face detection, skin texture, EXIF
tests/
├── conftest.py             # Shared async client + DB init fixture
├── test_api.py             # Health, swagger, OpenAPI schema tests
├── test_audio.py           # Audio upload + validation tests
├── test_image.py           # Image upload + validation tests
└── test_scans.py           # Scan history, provenance, dashboard tests
docs/
├── PRD.md                  # Product requirements, user stories, NFRs
├── TECH_SPEC.md            # Architecture, data models, ML strategy
├── API_SPEC.md             # All endpoint contracts, error codes, severity logic
└── SPEC_INDEX.md           # Module-to-spec mapping
scripts/
├── benchmark_image.py      # Image benchmark: accuracy, precision, recall, F1, per-model breakdown
├── benchmark_audio.py      # Audio benchmark: accuracy, precision, recall, F1
├── benchmark_results.json  # Saved image benchmark results
└── benchmark_audio_results.json  # Saved audio benchmark results
```

## Development Methodology

**Spec-driven development:** Read spec → implement to spec → validate against spec → update spec if needed.

Specs are in `docs/` (PRD, TECH_SPEC, API_SPEC, SPEC_INDEX).

## How to Run

```bash
source venv/bin/activate
uvicorn app.main:app --reload
# Dashboard: http://localhost:8000
# Swagger:   http://localhost:8000/docs
# Health:    http://localhost:8000/health
```

## How to Test

```bash
source venv/bin/activate
python -m pytest tests/ -v
```

13 tests covering: health check, swagger docs, OpenAPI schema, audio detection (upload + validation + analysis fields), image detection (upload + validation + analysis fields), scan history, provenance, dashboard serving.

## Architecture Decisions

- **Image detection uses a dual-model ensemble:** Two complementary ML models (CommunityForensics ViT + prithivMLmods SigLIP) run on each image. Their fake-probabilities are averaged with equal weight (50/50). When models disagree (one says fake, other says real), a disagreement bonus boosts the fake probability since this pattern is characteristic of AI-generated content that falls in different models' blind spots.
- **Three-signal verdict system:** Final verdict combines ML ensemble output (70% weight) with rule-based feature analysis (30% weight). Strong rule-based signals (3+ suspicious indicators like smooth skin + stripped EXIF + high symmetry) can override a weak model "real" verdict. When the model is unsure (<0.4 confidence), rule-based analysis dominates.
- **Graceful degradation:** If one ML model fails to load, the other runs alone. If both fail, detection still works via rule-based analysis. If Claude API fails, pre-written fallback explanations are used.
- **Singleton services:** `audio_detector` and `image_detector` are module-level singletons loaded once at startup.
- **CommunityForensics preprocessing workaround:** The model's `AutoImageProcessor` resizes to 440px then center-crops to 384px, but the crop step doesn't execute correctly, causing a dimension mismatch crash (440 not divisible by patch_size=16). Fixed by manually resizing to 384x384 and normalizing with the model's trained mean/std values.
- **Audio model is Wav2Vec2-Large-XLSR** — 300M params, 24 layers, 53 languages. Uses `AutoModelForAudioClassification` (garystafford/wav2vec2-deepfake-voice-detector). Labels: `{0: real, 1: fake}`. Trained on modern TTS (ElevenLabs, Amazon Polly, Kokoro, Speechify, Hume AI).

## Image Detection: Rule-Based Feature Analysis

The `image_features.py` module extracts these signals:

| Feature | Method | Suspicious Threshold |
|---|---|---|
| GAN artifacts | FFT frequency analysis | `freq_std < 2.0 && high_freq_ratio > 0.7` |
| Frequency anomalies | FFT magnitude distribution | "high_frequency_grid_pattern" |
| Facial symmetry | Haar cascade face detection + left/right half comparison | `> 0.95` (too symmetric) |
| Skin smoothness | Laplacian variance on face region (detects lack of pores/texture) | `> 0.85` (suspiciously smooth) |
| Lighting consistency | Brightness variance across image quadrants | `< 0.65` (inconsistent) |
| EXIF metadata | PIL EXIF tag inspection | "exif_stripped" (no camera tags) |

The **skin smoothness** metric is specifically designed to catch StyleGAN/GAN-generated faces which lack natural skin texture (pores, fine lines). Real faces typically score 0.3–0.7, GAN faces score 0.85–0.99.

## Environment Variables

See `.env.example`. Key ones:
- `ANTHROPIC_API_KEY` — Required for AI explanations (falls back to templates without it)
- `MODEL_AUDIO` — HuggingFace model ID for audio detection
- `MODEL_IMAGE` — HuggingFace model ID for primary image model (CommunityForensics)
- `MODEL_IMAGE_ENSEMBLE` — HuggingFace model ID for secondary image model (prithivMLmods)

## What's Built (All 5 Modules Complete)

1. **Voice Deepfake Detector** — Audio upload, Librosa feature extraction (MFCCs, pitch, breathing, spectral), Wav2Vec2 model inference, verdict + confidence + severity
2. **Image Deepfake Detector** — Image upload, OpenCV feature extraction (FFT/GAN artifacts, face detection, symmetry, skin texture, lighting, EXIF), dual-model ensemble inference (CommunityForensics ViT + prithivMLmods SigLIP), disagreement-aware verdict combining
3. **AI Threat Explainer** — Claude API generates plain-English explanations with severity scoring and MITRE ATLAS mapping; template fallback when API unavailable
4. **C2PA Content Credentials Viewer** — Checks media for C2PA manifests (verified/none/tampered), displays creator tool + edit history + AI generation flags, EU AI Act notes
5. **Dashboard & Integration** — Dark theme web UI with drag-drop upload, confidence gauges, scan history table, Swagger docs at /docs

## Benchmark

### Image Detection

Measured against `itsLeen/deepfake_vs_real_image_detection` (512x512+ images, 100 real + 100 fake, seed=42). Script: `scripts/benchmark_image.py`.

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| **Full Pipeline** (Ensemble + Rules) | 55.5% | 54.6% | 65.0% | 0.594 |
| CommunityForensics ViT | 46.5% | — | — | 0.462 |
| prithivMLmods SigLIP | 51.0% | — | — | 0.364 |

Key finding: the full pipeline outperforms either individual model, confirming the ensemble + rule-based approach compensates for each model's blind spots. Main weakness is false positives (54% of real images flagged as fake), primarily driven by the rule-based system firing on legitimate photos with stripped EXIF or smooth skin. Results saved to `scripts/benchmark_results.json`.

### Audio Detection

Measured against `UniDataPro/real-vs-fake-human-voice-deepfake-audio` (44.1kHz, ~48s clips, 14 real + 14 fake, seed=42). Script: `scripts/benchmark_audio.py`.

| Metric | Score |
|---|---|
| Accuracy | 50.0% |
| Precision | 50.0% |
| Recall | 57.1% |
| F1 | 0.533 |

Key finding: audio detection is near coin-flip on this dataset. The Wav2Vec2 model struggles to differentiate real vs fake voices in this particular dataset, suggesting the fake voices may use TTS engines not covered by the model's training data or the model needs fine-tuning. Results saved to `scripts/benchmark_audio_results.json`.

## How to Run Benchmarks

```bash
source venv/bin/activate
pip install datasets soundfile  # if not installed
python scripts/benchmark_image.py [--sample N]  # default: 100 per class
python scripts/benchmark_audio.py [--sample N]  # default: 50 per class
```

## Known Limitations

- No video deepfake detection (out of scope for MVP)
- c2pa-python is optional — requires separate install
- Audio model is ~1.2GB (wav2vec2-large-xlsr, 300M params) — larger than typical base models
- Models download from HuggingFace on first startup (~2GB total for both image models + audio model)
- AI-generated landscapes/scenes without faces or human subjects are extremely hard to detect — no open-source model reliably catches these
- prithivMLmods model is trained primarily on diffusion-generated images (DALL-E, Stable Diffusion) and struggles with GAN-generated faces (StyleGAN); CommunityForensics covers this gap via the ensemble
- Individual model confidences can be low on borderline images — the ensemble + rule-based combiner compensates but final confidence may be ~50%
- Benchmark accuracy (55.5% image, 50.0% audio) leaves room for improvement via threshold tuning, weight optimization, model fine-tuning, and relaxing rule-based false positive triggers
