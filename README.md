---
title: DeepFakeGuard
emoji: 🛡️
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# DeepFakeGuard

**AI-Powered Deepfake Detection Toolkit** — Detect AI-generated voices and manipulated images via a REST API, get plain-English threat explanations powered by Claude, and verify media provenance with C2PA Content Credentials.

![Python 3.12](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Features

- **Voice Deepfake Detection** — Upload audio, get a real/synthetic verdict with confidence. Uses Wav2Vec2-Large-XLSR (300M params, 53 languages) trained on modern TTS engines (ElevenLabs, Amazon Polly, Kokoro, Speechify).
- **Image Deepfake Detection** — Dual-model ensemble (CommunityForensics ViT + prithivMLmods SigLIP) combined with rule-based feature analysis (GAN artifact detection, facial symmetry, skin texture, EXIF metadata).
- **AI Threat Explanations** — Claude generates plain-English explanations with severity scoring and MITRE ATLAS mapping. Falls back to templates when API is unavailable.
- **C2PA Content Credentials** — Check media for C2PA manifests, view creator tool, edit history, and AI generation flags.
- **Web Dashboard** — Dark-themed drag-and-drop UI with confidence gauges and scan history.

## Architecture

```
                    ┌──────────────┐
                    │   Dashboard   │  (HTML + Tailwind)
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   FastAPI     │  REST API + Swagger
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐ ┌──▼───────┐ ┌──▼───────┐
       │   Audio     │ │  Image   │ │   C2PA   │
       │  Detector   │ │ Detector │ │Verifier  │
       └──────┬──────┘ └──┬───────┘ └──────────┘
              │            │
       ┌──────▼──────┐ ┌──▼───────────────┐
       │  Wav2Vec2   │ │  Ensemble Engine  │
       │  (300M)     │ │ ViT + SigLIP +   │
       │             │ │ Rule-Based       │
       └─────────────┘ └──────────────────┘
              │            │
              └─────┬──────┘
                    │
             ┌──────▼──────┐
             │   Claude    │  AI Explanations
             │     API     │
             └─────────────┘
```

## Quick Start

```bash
# Clone
git clone https://github.com/noorullah1102/DeepFakeGuard.git
cd DeepFakeGuard

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY (optional — falls back to templates)

# Run
uvicorn app.main:app --reload
```

- **Dashboard:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

> First startup downloads ML models from HuggingFace (~2GB total). Subsequent runs use cached models.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/detect/audio` | Upload audio file for deepfake analysis |
| `POST` | `/api/v1/detect/image` | Upload image for deepfake analysis |
| `POST` | `/api/v1/provenance` | Check C2PA content credentials |
| `GET` | `/api/v1/scans` | List scan history |
| `GET` | `/api/v1/scans/{id}` | Get specific scan result |
| `GET` | `/health` | System health + model status |
| `GET` | `/docs` | Interactive Swagger documentation |

### Example Response

```json
{
  "verdict": "synthetic",
  "confidence": 0.87,
  "severity": "high",
  "explanation": "This image shows multiple indicators of AI generation...",
  "analysis": {
    "ensemble_prediction": { "fake_probability": 0.89, "models_agree": true },
    "feature_analysis": { "suspicious_indicators": ["smooth_skin", "stripped_exif", "high_symmetry"] },
    "model_details": {
      "communityforensics_vit": { "label": "fake", "confidence": 0.91 },
      "prithivmlmods_siglip": { "label": "Fake", "confidence": 0.86 }
    }
  }
}
```

## How It Works

### Image Detection — Three-Signal Verdict System

1. **ML Ensemble (70% weight)** — Two models vote independently:
   - **CommunityForensics ViT** — Catches GAN-generated faces (StyleGAN)
   - **prithivMLmods SigLIP** — Catches diffusion-generated images (DALL-E, Stable Diffusion)
   - When models disagree, a disagreement bonus boosts fake probability (characteristic of AI content in different models' blind spots)

2. **Rule-Based Analysis (30% weight)** — Traditional CV feature extraction:
   - FFT frequency analysis for GAN artifacts
   - Facial symmetry detection (too perfect = suspicious)
   - Skin texture smoothness (lack of pores = GAN face)
   - Lighting consistency across quadrants
   - EXIF metadata inspection (stripped tags = red flag)

3. **Final Verdict** — Weighted combination. Strong rule-based signals (3+ indicators) can override a weak model "real" verdict.

### Audio Detection

- Librosa feature extraction (MFCCs, spectrograms, pitch contour, breathing patterns)
- Wav2Vec2-Large-XLSR inference (24-layer transformer, trained on modern TTS)
- Combined analysis produces verdict + confidence + severity

## Benchmark Results

### Image Detection

Tested on [`itsLeen/deepfake_vs_real_image_detection`](https://huggingface.co/datasets/itsLeen/deepfake_vs_real_image_detection) (100 real + 100 fake, seed=42). Script: `scripts/benchmark_image.py`.

| Model | Accuracy | Precision | Recall | F1 |
|-------|----------|-----------|--------|----|
| **Full Pipeline** (Ensemble + Rules) | **55.5%** | 54.6% | 65.0% | **0.594** |
| CommunityForensics ViT alone | 46.5% | — | — | 0.462 |
| prithivMLmods SigLIP alone | 51.0% | — | — | 0.364 |

<details>
<summary>Key findings</summary>

- The full pipeline **outperforms either model individually** (+9% over ViT, +4.5% over SigLIP), confirming the ensemble + rule-based approach compensates for each model's blind spots.
- Main weakness is **false positives** (54% of real images flagged as fake), primarily driven by the rule-based system firing on legitimate photos with stripped EXIF or smooth skin.
- CommunityForensics ViT struggles with images outside its training distribution (non-fake samples it hasn't seen).
- prithivMLmods SigLIP is trained primarily on diffusion-generated images and misses GAN-generated faces.
</details>

### Audio Detection

Tested on [`UniDataPro/real-vs-fake-human-voice-deepfake-audio`](https://huggingface.co/datasets/UniDataPro/real-vs-fake-human-voice-deepfake-audio) (14 real + 14 fake, seed=42). Script: `scripts/benchmark_audio.py`.

| Metric | Score |
|--------|-------|
| Accuracy | 50.0% |
| Precision | 50.0% |
| Recall | 57.1% |
| F1 | 0.533 |

<details>
<summary>Key findings</summary>

- Audio detection is near **coin-flip** on this dataset. The Wav2Vec2 model struggles to differentiate real vs fake voices, suggesting the fake voices may use TTS engines not covered by the model's training data.
- The model was trained on ElevenLabs, Amazon Polly, Kokoro, and Speechify — other TTS engines may produce different artifacts.
- Room for improvement via threshold tuning, domain-specific fine-tuning, and expanding training data coverage.
</details>

> **Why share these numbers?** Deepfake detection is an adversarial arms race. No open-source tool reliably catches everything. Being transparent about benchmark performance builds trust and sets realistic expectations. Results are saved to `scripts/benchmark_results.json` and `scripts/benchmark_audio_results.json`.

### Reproduce Benchmarks

```bash
source venv/bin/activate
pip install datasets soundfile  # if not installed
python scripts/benchmark_image.py [--sample N]  # default: 100 per class
python scripts/benchmark_audio.py [--sample N]  # default: 50 per class
```

## Testing

```bash
python -m pytest tests/ -v
```

13 tests covering health check, Swagger docs, OpenAPI schema, audio/image detection (upload + validation + analysis), scan history, provenance, and dashboard.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| API | FastAPI |
| Audio ML | PyTorch + Wav2Vec2-Large-XLSR |
| Image ML | CommunityForensics ViT + prithivMLmods SigLIP |
| AI Explanations | Claude API (Anthropic SDK) |
| Provenance | c2pa-python |
| Database | SQLite |
| Frontend | HTML + Tailwind CSS + Vanilla JS |
| Testing | pytest + pytest-asyncio + httpx |

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | No | — | Enables AI explanations (template fallback without it) |
| `MODEL_AUDIO` | No | `garystafford/wav2vec2-deepfake-voice-detector` | HuggingFace audio model |
| `MODEL_IMAGE` | No | `buildborderless/CommunityForensics-DeepfakeDet-ViT` | Primary image model |
| `MODEL_IMAGE_ENSEMBLE` | No | `prithivMLmods/deepfake-detector-model-v1` | Secondary image model |

## License

MIT
