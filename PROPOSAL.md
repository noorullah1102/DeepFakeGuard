# DeepFakeGuard — AI-Powered Deepfake Detection Toolkit

> "Humans detect deepfakes 55% of the time — barely better than a coin flip. This tool gives defenders an actual edge."

## Background

In 2025-2026, deepfakes have crossed from novelty to existential corporate threat. Reddit's security communities, Fortune 500 incident reports, and government advisories all converge on one message: **the tools to create deepfakes are cheap, fast, and accessible — but the tools to detect them barely exist outside research labs.**

### The Conversations Happening Right Now

#### 1. Deepfakes Are Now a Billion-Dollar Fraud Vector

The numbers are staggering and accelerating:

- Deepfake files surged from **500,000 (2023) to 8 million (2025)** — a 1,500% increase ([Keepnet](https://keepnetlabs.com/blog/deepfake-statistics-and-trends), [DeepStrike](https://deepstrike.io/blog/deepfake-statistics-2025))
- Deepfake fraud attempts increased **2,137% over three years**, now accounting for 6.5% of all fraud attempts ([Bright Defense](https://www.brightdefense.com/resources/deepfake-statistics/))
- Projected losses exceeded **$1 billion in 2025** — $200M in Q1 alone, $347M in Q2 ([SQ Magazine](https://sqmagazine.co.uk/deepfake-statistics/))
- **85% of organizations** experienced at least one deepfake-related incident in the past 12 months
- Fintech saw a **700% increase** in deepfake incidents
- The deepfake detection market is projected to grow from $5.5B (2023) to $15.7B (2026) at 42% CAGR

Fortune declared: [*"2026 will be the year you get fooled by a deepfake"*](https://fortune.com/2025/12/27/2026-deepfakes-outlook-forecast/). Voice cloning has crossed the "indistinguishable threshold."

#### 2. The $25M Arup Heist — The Attack That Changed Everything

In February 2024, a finance worker at British engineering firm Arup was tricked into transferring **$25 million** across 15 transactions to 5 bank accounts. The attack? A video call where **every other participant — including the "CFO" — was an AI-generated deepfake** built from publicly available footage of real executives.

The worker initially suspected phishing. But when he joined the video call and saw his colleagues' faces and heard their voices, he was convinced. He authorized every transfer.

- [CNN: Finance worker pays out $25 million after video call with deepfake CFO](https://www.cnn.com/2024/02/04/asia/deepfake-cfo-scam-hong-kong-intl-hnk)
- [Fortune: A deepfake 'CFO' tricked British design firm Arup in $25 million fraud](https://fortune.com/europe/2024/05/17/arup-deepfake-fraud-scam-victim-hong-kong-25-million-cfo/)
- [CFO Dive: Scammers siphon $25M via AI deepfake CFO](https://www.cfodive.com/news/scammers-siphon-25m-engineering-firm-arup-deepfake-cfo-ai/716501/)

This was the moment deepfakes stopped being a curiosity and became a board-level concern.

#### 3. Voice Cloning Is Hitting Companies Every Week

The Arup heist wasn't isolated. Voice cloning attacks are now routine:

- **Ferrari (July 2024):** An executive received a WhatsApp call from a convincing AI clone of CEO Benedetto Vigna's voice, complete with his southern Italian accent, requesting an urgent currency-hedge transaction. The exec foiled it by asking about a book Vigna had recently recommended. The caller hung up. ([Fortune](https://fortune.com/2024/07/27/ferrari-deepfake-attempt-scammer-security-question-ceo-benedetto-vigna-cybersecurity-ai/), [MIT Sloan](https://sloanreview.mit.edu/article/how-ferrari-hit-the-brakes-on-a-deepfake-ceo/))
- **Wiz (late 2024):** Attackers cloned CEO Assaf Rappaport's voice and sent voicemails to dozens of employees requesting credentials
- **WPP (attempted):** Fake Teams meeting with voice-cloned senior executive and edited YouTube footage
- **Italy corporate wave (early 2025):** Coordinated attacks targeting Giorgio Armani and other business leaders, impersonating the Italian defence minister
- **Singapore multinational (March 2025):** Finance director tricked via deepfake Zoom call with multiple fake executives

Banks lose an average of **$600,000 per voice deepfake incident**; 23% lose over $1M. Deepfake vishing attacks surged **1,633% in Q1 2025** vs Q4 2024. ([Right-Hand](https://right-hand.ai/blog/deep-fake-vishing-attacks-2025/), [SQ Magazine](https://sqmagazine.co.uk/ai-voice-cloning-fraud-statistics/))

#### 4. KnowBe4 Hired a Deepfake — And They're a Security Company

In July 2024, [KnowBe4](https://blog.knowbe4.com/how-a-north-korean-fake-it-worker-tried-to-infiltrate-us) — a cybersecurity awareness training company — hired a software engineer who passed **4 video interviews, background checks, and reference verification.** He was actually a North Korean operative using a stolen US identity and an AI-enhanced stock photo.

The fake worker had the laptop shipped to a "mule laptop farm" and VPN'd in from North Korea during US night hours. He was detected within 25 minutes of deploying malware, and no data was breached thanks to restricted onboarding permissions. But the damage to trust was done.

Dozens of other organizations — Fortune 500 to 12-person firms — contacted KnowBe4 with similar stories. Pindrop now estimates **1 in 4 North Korean IT job applicants use deepfakes** to conceal their identity.

- [KnowBe4 Blog: How a North Korean Fake IT Worker Tried to Infiltrate Us](https://blog.knowbe4.com/how-a-north-korean-fake-it-worker-tried-to-infiltrate-us)
- [CyberScoop: KnowBe4 hired a fake IT worker from North Korea](https://cyberscoop.com/cyber-firm-knowbe4-hired-a-fake-it-worker-from-north-korea/)
- [iProov: The KnowBe4 Deepfake Incident](https://www.iproov.com/blog/knowbe4-deepfake-wake-up-call-remote-hiring-security)

#### 5. Deepfake-as-a-Service Is Now a Commodity

The barrier to entry has collapsed. Deepfake creation is now a service industry on the dark web:

- Deepfake image service: **$10–$50**
- Synthetic identity: **up to $15**
- Voice cloning: **under $10/month**
- A convincing 60-second deepfake video: **produced in under 25 minutes at zero cost**
- AI tools dominate **60% of dark web cyber listings** in 2025
- Underground forums recruit "AI video actors," "deepfake presenters," and "virtual call agents"

([Cyble](https://cyble.com/knowledge-hub/deepfake-as-a-service-exploded-in-2025/), [Dark Reading](https://www.darkreading.com/threat-intelligence/deepfake-apps-explode-multimillion-dollar-corporate-heists), [Kaspersky](https://www.kaspersky.com/blog/deepfake-darknet-market/48112/))

#### 6. Humans Can't Detect Deepfakes — And They Think They Can

A meta-analysis of 67 studies found overall human detection accuracy at **55.54%** — barely above a coin flip ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2451958824001714)). Yet **60% of people think they can spot deepfakes.**

Breakdown:
- High-quality video deepfakes: humans detect only **24.5%**
- Images: ~62% accuracy
- Audio: humans mistake AI voices for real **~80% of the time** in short clips
- iProov 2025 study: only **0.1% of participants** correctly identified all fakes

Meanwhile, widely available detection tools catch only **~65% of deepfakes** in real-world conditions — state-of-the-art lab systems hit 94-96% but accuracy drops 45-50% on unseen manipulations ([Ceartas](https://blog.ceartas.io/p/deepfake-detection-accuracy)).

**The gap:** Detection tools exist in research papers and enterprise products. Almost nothing exists for small security teams, developers, or analysts who need a practical, explainable detection API. And regulators are about to mandate it.

#### 7. Regulation Is Coming — The EU AI Act Mandates Deepfake Labeling

The [EU AI Act (Article 50)](https://artificialintelligenceact.eu/article/50/) requires:
- AI systems generating synthetic audio/image/video must ensure outputs are **marked in machine-readable format** and detectable as AI-generated
- Deployers using AI to create deepfakes must disclose this **"clearly and distinguishably"**
- Transparency obligations take effect **August 2026**
- Draft Code of Practice proposes persistent visual indicators, opening disclaimers for live video, and an interim "AI" icon

This creates immediate demand for tools that can **verify content provenance and detect synthetic media** — exactly what DeepFakeGuard does.

## What DeepFakeGuard Does

### Core Modules

| # | Module | Description | Key Tech |
|---|--------|-------------|----------|
| 1 | **Voice Deepfake Detector** | Upload audio, get verdict (real/synthetic) with confidence score and artifact analysis (spectral anomalies, unnatural pitch, cloned voice patterns) | PyTorch, Librosa, Wav2Vec2 (HuggingFace) |
| 2 | **Image Authenticity Checker** | Upload a photo, detect GAN artifacts, inconsistent lighting, blending boundaries, frequency-domain anomalies | PyTorch, OpenCV, ViT (HuggingFace) |
| 3 | **AI Explanation Engine** | Sends detection results to Claude API, generates plain-English reports — *what* was detected, *why* it matters, *how confident* the system is | Claude API (Anthropic SDK) |
| 4 | **C2PA Credential Viewer** | Check if media has Content Credentials — the emerging standard for content provenance backed by Adobe, Google, Microsoft, and OpenAI | c2pa-python, JSON parsing |
| 5 | **REST API + Dashboard** | Full API with Swagger docs, simple web dashboard showing scan results, confidence visualizations, and detection trends | FastAPI, HTML + Tailwind + vanilla JS |

### Example Flow

```
User uploads audio: ceo_urgent_call.wav

DeepFakeGuard responds:
{
  "verdict": "synthetic",
  "confidence": 0.91,
  "media_type": "audio",
  "analysis": {
    "spectral_artifacts": true,
    "pitch_consistency": 0.43,
    "breathing_patterns": "absent",
    "background_noise": "unnaturally_uniform",
    "codec_artifacts": "consistent_with_tts"
  },
  "c2pa_credentials": null,
  "ai_explanation": "This audio shows multiple indicators of AI generation.
    The pitch remains unnaturally consistent across the 47-second clip —
    real human speech fluctuates significantly more. There are no natural
    breathing patterns between sentences, and the background noise is
    suspiciously uniform (real recordings have varying ambient sound).
    The spectral analysis reveals smoothing artifacts consistent with
    text-to-speech or voice cloning tools. This is likely a cloned voice,
    not a recording of the actual speaker.",
  "severity": "high",
  "action": "Do not act on any instructions from this call. Verify the speaker's identity through a known, separate channel. Report to security team.",
  "mitre_atlas": "AML.T0048 — Deepfake"
}
```

```
User uploads image: executive_headshot.jpg

DeepFakeGuard responds:
{
  "verdict": "manipulated",
  "confidence": 0.87,
  "media_type": "image",
  "analysis": {
    "gan_artifacts": true,
    "frequency_anomalies": "high_frequency_grid_pattern",
    "facial_symmetry": "abnormally_perfect",
    "lighting_consistency": 0.62,
    "metadata_integrity": "exif_stripped"
  },
  "c2pa_credentials": null,
  "ai_explanation": "This headshot shows signs of AI generation or heavy
    manipulation. The facial symmetry is abnormally perfect — real faces
    have subtle asymmetries. Frequency-domain analysis reveals a faint
    grid pattern characteristic of GAN-generated images. The EXIF metadata
    has been completely stripped, which is common in AI-generated images
    that never passed through a real camera. This may be a synthetic
    identity photo — similar to those used in the KnowBe4 North Korean
    operative incident.",
  "severity": "high",
  "action": "Do not use this image for identity verification. Request a live video verification with liveness detection.",
  "mitre_atlas": "AML.T0048.002 — Deepfake (Visual Media)"
}
```

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Language | Python 3.11+ | Industry standard for ML and security tooling |
| API Framework | FastAPI | Async support, auto-generated Swagger docs, consistent with PhishRadar |
| Audio ML | PyTorch + Librosa | Spectrogram extraction, MFCC features, waveform analysis |
| Audio Model | Wav2Vec2-based (HuggingFace) | Pre-trained on ASVspoof, state-of-the-art voice anti-spoofing |
| Image ML | PyTorch + OpenCV | Face extraction, frequency analysis, GAN artifact detection |
| Image Model | ViT-based (HuggingFace) | Pre-trained deepfake image classifier, ~92% accuracy |
| AI | Claude API (Anthropic SDK) | Threat explanation, plain-English reports |
| Provenance | c2pa-python | Parse C2PA Content Credentials metadata |
| Database | SQLite (MVP) | Scan history, detection trends |
| Frontend | HTML + Tailwind + vanilla JS | Dashboard, no framework overhead |

## Active Research & Benchmarks (2024-2026)

Deepfake detection is one of the most active research areas in AI security right now. Here are the key datasets, benchmarks, and competitions your brother should know about — and which ones each module will use.

### Audio Deepfake Detection

| Dataset | Year | Size | What's Special | Use In Project |
|---------|------|------|----------------|----------------|
| **ASVspoof 5** | 2024 | Crowdsourced, 4000+ speakers, diverse acoustic conditions | Latest edition of the gold-standard voice anti-spoofing challenge. First to include **adversarial attacks**. Two tracks: standalone countermeasures (Track 1) and spoofing-robust speaker verification (Track 2). Baseline models provided (RawNet2, AASIST). Metrics: minDCF, EER, CLLR. | **Module 1 primary dataset** |
| **MLAAD v9** | Jan 2026 | 678.3 hours of synthetic speech, **51 languages**, 140 TTS models (78 architectures) | Addresses the critical gap that most datasets are English/Chinese only. Outperforms InTheWild and Fake-Or-Real as training data. Alternately outperforms ASVspoof 2019 across 8 test datasets — they're complementary. | **Module 1 supplementary** — test multilingual generalization |
| **ASVspoof 2019 LA** | 2019 | 12,483 bonafide + 108,978 spoofed utterances | Still the most widely-used benchmark. First to combine TTS, voice conversion, and replay attacks. Best published EER: 4.98%. | **Module 1 baseline comparison** |

**Key research:** Wav2Vec2 and WavLM model families are currently state-of-the-art for audio deepfake detection ([HuggingFace blog](https://huggingface.co/blog/Andyrasika/deepfake-detect), [PyData Global 2024](https://global2024.pydata.org/cfp/talk/LJPSKA/)). Off-the-shelf HuggingFace models can achieve competitive results without training from scratch.

**Available pre-trained models:**
- [MelodyMachine/Deepfake-audio-detection-V2](https://huggingface.co/MelodyMachine/Deepfake-audio-detection-V2) — Fine-tuned audio deepfake detector
- [mo-thecreator/Deepfake-audio-detection](https://huggingface.co/mo-thecreator/Deepfake-audio-detection) — Wav2Vec2-based
- [Hemgg/Deepfake-audio-detection](https://huggingface.co/Hemgg/Deepfake-audio-detection) — Trained on multi-ethnic English dataset

### Image/Face Deepfake Detection

| Dataset | Year | Size | What's Special | Use In Project |
|---------|------|------|----------------|----------------|
| **DF40** | 2024 (NeurIPS) | Million-level images + videos, ~143GB total | The most comprehensive benchmark: **40 deepfake techniques** across 4 categories (face-swap, face-reenactment, entire face synthesis, face editing). Includes SOTA generators like MidJourney 6, Stable Diffusion, HeyGen. 10 pre-trained detection model checkpoints released. | **Module 2 primary benchmark** |
| **OpenFake** | Sep 2025 | ~4M images (3M real + 1M synthetic) | Politically grounded dataset with **crowdsourced adversarial platform** for continuous updates. Tests on in-the-wild social media. Detectors trained on OpenFake show strong generalization to unseen generators. CC BY-NC-SA 4.0 license. | **Module 2 supplementary** — real-world generalization |
| **DeepfakeBench** | 2023 (NeurIPS) | 9 datasets unified, 36 detection methods | Not a dataset but a **unified evaluation framework**. Standardized preprocessing, LMDB format, DDP training. Includes 36 detection methods (spatial, frequency, video). Cross-dataset evaluation with pretrained weights. | **Module 2 evaluation framework** |

**Key research:** DF40 showed that current detectors trained on old datasets (FaceForensics++) **fail catastrophically** on modern generators like MidJourney and Stable Diffusion. Models must be retrained on current-generation synthetic media. UCF achieves 0.9527 average AUC within-domain but drops to 0.77-0.78 cross-dataset.

**Available pre-trained models:**
- [prithivMLmods/Deep-Fake-Detector-v2-Model](https://huggingface.co/prithivMLmods/Deep-Fake-Detector-v2-Model) — ViT-based, 92.12% accuracy
- [prithivMLmods/deepfake-detector-model-v1](https://huggingface.co/prithivMLmods/deepfake-detector-model-v1) — Fine-tuned from SigLIP

### Multimodal (Audio-Visual)

| Dataset | Year | Size | What's Special | Use In Project |
|---------|------|------|----------------|----------------|
| **AV-Deepfake1M** | 2024 (ACM MM) | 1M+ videos, 2000+ subjects | First large-scale audio-visual deepfake dataset. Focuses on **localizing small manipulated segments** embedded in real videos — much harder than whole-video classification. Benchmarks show significant performance drops vs. previous datasets. | **Stretch goal** — multimodal detection |

### Detection Accuracy Context

Understanding the state of the art helps set realistic expectations:

| Metric | Score | Source |
|--------|-------|--------|
| Human accuracy (meta-analysis, 67 studies) | **55.54%** | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2451958824001714) |
| Human on high-quality video deepfakes | **24.5%** | [Wiley](https://onlinelibrary.wiley.com/doi/10.1155/hbe2/1833228) |
| Human on short AI voice clips | **~20%** correct detection | [Bright Defense](https://www.brightdefense.com/resources/deepfake-statistics/) |
| Best lab-condition AI detectors | **94-96%** | [Ceartas](https://blog.ceartas.io/p/deepfake-detection-accuracy) |
| UC San Diego universal detector (Aug 2025) | **98%** | [TTMS](https://ttms.com/deepfake-detection-breakthrough-universal-detector-achieves-98-accuracy/) |
| Real-world effectiveness drop vs lab | **-45 to -50%** | [Ceartas](https://blog.ceartas.io/p/deepfake-detection-accuracy) |
| Widely available tools | **~65%** | [Ceartas](https://blog.ceartas.io/p/deepfake-detection-accuracy) |
| DeepfakeBench top cross-dataset AUC | **0.77-0.78** | [DeepfakeBench](https://github.com/SCLBD/DeepfakeBench) |

**The takeaway:** Even a tool that achieves 70-80% accuracy in the wild would be significantly better than human performance. The goal isn't perfection — it's giving defenders a meaningful advantage over guessing.

## Build Plan — One Module at a Time

The project is structured as **5 independent modules**, each self-contained with its own deliverable, dataset, and portfolio story. Your brother can ship and demo each module before starting the next. Each module builds on the shared FastAPI skeleton but adds a distinct capability.

### Module 1 — Voice Deepfake Detector
*Estimated: 3-4 weeks | Deliverable: Working API endpoint that classifies audio as real/synthetic*

**What he'll build:**
- [ ] Project structure, virtual environment, FastAPI skeleton with health check
- [ ] File upload endpoint (accepts .wav, .mp3, .flac)
- [ ] Audio feature extraction with Librosa (spectrograms, MFCCs, pitch tracking, zero-crossing rate)
- [ ] Basic rule-based checks (breathing pattern detection, background noise uniformity, pitch variance scoring)
- [ ] Download ASVspoof 5 dataset (Track 1) — register at [asvspoof.org](https://www.asvspoof.org/)
- [ ] Fine-tune a Wav2Vec2-based model from HuggingFace on ASVspoof 5
- [ ] Alternatively: start with a pre-trained model like [MelodyMachine/Deepfake-audio-detection-V2](https://huggingface.co/MelodyMachine/Deepfake-audio-detection-V2) and evaluate on ASVspoof
- [ ] Evaluation: Equal Error Rate (EER), precision, recall, ROC curves, minDCF
- [ ] Test on MLAAD v9 samples to check multilingual generalization
- [ ] Integrate classifier into FastAPI `/api/v1/detect/audio` endpoint
- [ ] Return structured JSON: verdict, confidence, feature breakdown
- [ ] Unit tests for audio preprocessing and API endpoint
- [ ] Write brief README section for this module

**What he'll learn:** PyTorch inference, HuggingFace model loading, audio signal processing fundamentals, evaluation metrics used in real anti-spoofing research.

**Portfolio story:** *"I built a voice deepfake detector and evaluated it against ASVspoof 5 — the same benchmark used by researchers at Interspeech. Here's my EER score compared to the baselines."*

---

### Module 2 — Image Deepfake Detector
*Estimated: 3-4 weeks | Deliverable: Working API endpoint that classifies images as real/manipulated*

**What he'll build:**
- [ ] Image upload endpoint (accepts .jpg, .png, .webp)
- [ ] Face extraction pipeline with OpenCV/dlib (crop, align, normalize)
- [ ] Frequency-domain analysis module (FFT to detect GAN checkerboard artifacts)
- [ ] EXIF metadata integrity checker (detect stripped/inconsistent metadata)
- [ ] Download DF40 test set (~93GB) or start with a smaller subset
- [ ] Fine-tune ViT-based model from HuggingFace for deepfake image detection
- [ ] Alternatively: use [prithivMLmods/Deep-Fake-Detector-v2-Model](https://huggingface.co/prithivMLmods/Deep-Fake-Detector-v2-Model) (92% accuracy) and evaluate on DF40
- [ ] Cross-generator evaluation: test on images from generators NOT in training set
- [ ] Evaluation: AUC, accuracy, precision/recall per forgery type
- [ ] Integrate into FastAPI `/api/v1/detect/image` endpoint
- [ ] Return structured JSON: verdict, confidence, artifact breakdown, metadata analysis
- [ ] Unit tests for image preprocessing and API endpoint

**What he'll learn:** Computer vision fundamentals, frequency-domain analysis, Vision Transformers, the critical problem of cross-generator generalization (why lab accuracy ≠ real-world accuracy).

**Portfolio story:** *"I evaluated my detector against DF40's 40 different deepfake generators — including MidJourney 6 and Stable Diffusion. Here's where it excels and where it breaks down."*

---

### Module 3 — AI Threat Explainer
*Estimated: 2 weeks | Deliverable: Every detection result now comes with a plain-English explanation*

**What he'll build:**
- [ ] Claude API integration via Anthropic SDK
- [ ] Prompt engineering for structured threat reports:
  - What was detected (specific artifacts and anomalies)
  - Why it matters (severity, attack type, real-world context)
  - Confidence assessment (what the model is sure about vs uncertain)
  - Recommended action (block, verify, report)
- [ ] MITRE ATLAS threat mapping (e.g., AML.T0048 — Deepfake)
- [ ] Severity scoring algorithm (combines model confidence + artifact count + metadata signals)
- [ ] SQLite database for scan history (timestamp, verdict, confidence, explanation)
- [ ] `/api/v1/scans` endpoint to retrieve past scan results
- [ ] Prompt iteration: test explanations on non-technical friends/family — can they understand and act?

**What he'll learn:** Prompt engineering for structured output, API integration, the difference between detection and actionable intelligence (the same gap PhishRadar addresses for phishing).

**Portfolio story:** *"Most deepfake detectors output a number. Mine explains what it found in language a finance team can act on — because the Arup $25M heist wasn't stopped by a confidence score."*

---

### Module 4 — C2PA Content Credentials Viewer
*Estimated: 2 weeks | Deliverable: Check any image/audio/video for provenance metadata*

**What he'll build:**
- [ ] Install [c2pa-python](https://github.com/contentauth/c2pa-python) library
- [ ] Parse C2PA manifests from uploaded media files
- [ ] Extract and display: creator tool, creation date, edit history, AI generation flags
- [ ] Handle the three states: has credentials (show them), no credentials (flag as unverified), tampered credentials (alert)
- [ ] `/api/v1/provenance` endpoint
- [ ] Visual display of the credential chain (who created → what tool → what edits)
- [ ] Test with real C2PA-signed images (DALL-E 3 outputs have Content Credentials, Adobe Firefly images too)
- [ ] Explain EU AI Act Article 50 implications in the API response

**What he'll learn:** Content provenance standards, cryptographic signing/verification, the emerging regulatory landscape. This is cutting-edge — very few developers have hands-on C2PA experience.

**Portfolio story:** *"I built a tool that checks for C2PA Content Credentials — the standard backed by Adobe, Google, Microsoft, and OpenAI. With the EU AI Act mandating deepfake labeling by August 2026, this is about to become critical infrastructure."*

---

### Module 5 — Dashboard & Integration
*Estimated: 2-3 weeks | Deliverable: Web UI that ties everything together*

**What he'll build:**
- [ ] HTML + Tailwind dashboard (consistent with PhishRadar's frontend approach)
- [ ] Upload interface: drag-and-drop for audio/image files
- [ ] Results view: verdict badge, confidence gauge, artifact breakdown, AI explanation
- [ ] C2PA credential viewer: visual credential chain display
- [ ] Scan history: table of past scans with filtering and search
- [ ] Detection trends: chart showing scan volume, detection rates over time
- [ ] Side-by-side comparison: original image vs. analysis overlay (frequency heatmap, artifact highlights)
- [ ] Full Swagger API documentation
- [ ] README with architecture diagram, setup guide, screenshots
- [ ] Write integration tests (upload → detect → explain → store full pipeline)
- [ ] Record demo video walking through a real detection scenario

**What he'll learn:** Frontend fundamentals, data visualization, API documentation, how to present technical work for a non-technical audience.

**Portfolio story:** *"Here's a 2-minute demo of DeepFakeGuard catching a voice-cloned CEO and explaining exactly why it's fake."*

## How This Complements PhishRadar

| | PhishRadar | DeepFakeGuard |
|--|-----------|---------------|
| Attack vector | Email / URLs | Voice / Video / Images |
| Input type | Text and URL features | Audio and image signals |
| ML approach | Classical ML (scikit-learn) | Deep Learning (PyTorch) |
| Models | Random Forest / Gradient Boosting | Wav2Vec2, ViT (Transformers) |
| Framework ref | MITRE ATT&CK | MITRE ATLAS (AI-specific) |
| Data sources | PhishTank, URLhaus, Reddit | ASVspoof, FaceForensics++, HuggingFace |
| Unique angle | Explains *why* a URL is dangerous | Explains *why* media is fake |
| Shared stack | FastAPI, Claude API, Tailwind, Python, SQLite | Same — builds on existing skills |

Together they tell a story: **"I can defend against both text-based social engineering and multimedia-based deepfake attacks, using both classical ML and deep learning, with AI-powered explainability."**

## Target LinkedIn Post

> **I built an open-source deepfake detection toolkit. Here's what I found.**
>
> After reading about the $25M Arup deepfake heist, the Ferrari CEO voice clone, and KnowBe4 unknowingly hiring a North Korean operative with an AI-generated face — I realized: the tools to *create* deepfakes cost $10. The tools to *detect* them are locked in research labs.
>
> **DeepFakeGuard** is a Python + FastAPI toolkit that:
> - Detects AI-generated voices using models trained on the ASVspoof benchmark
> - Identifies manipulated images through GAN artifact and frequency analysis
> - Uses Claude AI to explain *why* something is fake — in plain English
> - Checks for C2PA Content Credentials (the new "nutrition label" for authentic media)
>
> Humans detect deepfakes 55% of the time. That's barely better than guessing. We need better tools — especially with the EU AI Act mandating synthetic media labeling by August 2026.
>
> 3 things I learned building this:
> 1. [Technical insight about audio feature engineering for voice anti-spoofing]
> 2. [Insight about the gap between lab accuracy and real-world detection]
> 3. [Insight about C2PA adoption and why content provenance matters]
>
> This is my second cybersecurity project — the first was PhishRadar (AI phishing detection). Together they cover text-based and multimedia-based AI threats.
>
> GitHub: [link]
>
> #cybersecurity #deepfake #python #AI #opensource #freshgrad

## What This Demonstrates to Employers

| Skill | Evidence |
|-------|----------|
| Deep learning | Fine-tuned Transformer models (Wav2Vec2, ViT) on benchmark datasets |
| Audio/signal processing | Spectrogram analysis, MFCC extraction, pitch tracking with Librosa |
| Computer vision | Face extraction, frequency analysis, GAN artifact detection with OpenCV |
| AI integration | Claude API for practical, explainable threat intelligence |
| Security fundamentals | MITRE ATLAS mapping, content provenance, threat severity assessment |
| Emerging standards | C2PA Content Credentials — ahead of EU AI Act compliance deadline |
| API design | FastAPI with documented endpoints, structured responses |
| Software engineering | Project structure, tests, documentation, version control |
| Communication | README, architecture docs, LinkedIn writeup |

## Resources & References

### Datasets & Benchmarks
- [ASVspoof 5](https://www.asvspoof.org/) — Latest voice anti-spoofing challenge (2024), crowdsourced data, adversarial attacks, baseline models ([GitHub](https://github.com/asvspoof-challenge/asvspoof5), [arXiv paper](https://arxiv.org/abs/2408.08739))
- [ASVspoof 2019 LA](https://www.asvspoof.org/) — Gold-standard voice anti-spoofing benchmark, 121K utterances, best published EER: 4.98% ([paper](https://arxiv.org/abs/1911.01601))
- [MLAAD v9](https://arxiv.org/abs/2401.09512) — Multi-Language Audio Anti-Spoofing Dataset (Jan 2026), 678 hours, 51 languages, 140 TTS models
- [DF40](https://github.com/YZY-stack/DF40) — 40 deepfake techniques, million-level images+videos, NeurIPS 2024. Includes MidJourney 6, Stable Diffusion, HeyGen ([paper](https://arxiv.org/abs/2406.13156))
- [OpenFake](https://arxiv.org/abs/2509.09495) — 4M images (3M real + 1M synthetic), politically grounded, crowdsourced adversarial platform (Sep 2025), CC BY-NC-SA 4.0
- [AV-Deepfake1M](https://arxiv.org/abs/2311.15308) — 1M+ audio-visual deepfake videos, 2000+ subjects, ACM MM 2024
- [DeepfakeBench](https://github.com/SCLBD/DeepfakeBench) — Unified evaluation framework, 9 datasets, 36 detection methods, NeurIPS 2023
- [FaceForensics++](https://github.com/ondyari/FaceForensics) — Classic benchmark for facial manipulation detection

### Pre-Trained Models (HuggingFace)
- [MelodyMachine/Deepfake-audio-detection-V2](https://huggingface.co/MelodyMachine/Deepfake-audio-detection-V2) — Fine-tuned audio deepfake detector
- [mo-thecreator/Deepfake-audio-detection](https://huggingface.co/mo-thecreator/Deepfake-audio-detection) — Wav2Vec2-based
- [Hemgg/Deepfake-audio-detection](https://huggingface.co/Hemgg/Deepfake-audio-detection) — Multi-ethnic English dataset
- [prithivMLmods/Deep-Fake-Detector-v2-Model](https://huggingface.co/prithivMLmods/Deep-Fake-Detector-v2-Model) — ViT-based, 92.12% accuracy
- [prithivMLmods/deepfake-detector-model-v1](https://huggingface.co/prithivMLmods/deepfake-detector-model-v1) — Fine-tuned from SigLIP
- [HuggingFace Blog: Detecting Deceptive Deep Fake Voices](https://huggingface.co/blog/Andyrasika/deepfake-detect)

### Libraries & APIs
- [c2pa-python](https://github.com/contentauth/c2pa-python) — C2PA Content Credentials library
- [Anthropic Claude API Docs](https://docs.anthropic.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Librosa Documentation](https://librosa.org/)
- [PyTorch](https://pytorch.org/)
- [OpenCV](https://opencv.org/)

### Open Source Deepfake Detection Tools
- [Deepfake-o-Meter v2.0](https://zinc.cse.buffalo.edu/ubmdfl/deep-o-meter/landing_page) — University at Buffalo, 18 detection algorithms, 445 users across 98 countries ([arXiv paper](https://arxiv.org/abs/2404.13146))
- [DeepSafe](https://github.com/siddharthksah/DeepSafe) — Enterprise-grade modular detection platform ([Medium overview](https://siddharthksah.medium.com/deepsafe-open-source-deepfake-detection-42f1c18f9500))

### Frameworks & Standards
- [MITRE ATLAS](https://atlas.mitre.org/) — AI threat landscape, 16 tactics, 84 techniques, 42 case studies ([CrowdStrike explainer](https://www.crowdstrike.com/en-us/cybersecurity-101/artificial-intelligence/mitre-atlas/))
- [C2PA Specification](https://c2pa.org/) — Content provenance standard, 200+ members including Adobe, Google, Microsoft, OpenAI ([How it works](https://contentauthenticity.org/how-it-works))
- [NSA/CISA Content Credentials Guidance (PDF)](https://media.defense.gov/2025/Jan/29/2003634788/-1/-1/0/CSI-CONTENT-CREDENTIALS.PDF) — Joint government advisory on media provenance
- [EU AI Act Article 50](https://artificialintelligenceact.eu/article/50/) — Deepfake transparency obligations (effective August 2026)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

### The Incidents That Inspired This

#### The Arup $25M Deepfake Heist
- [CNN: Finance worker pays out $25 million after video call with deepfake CFO](https://www.cnn.com/2024/02/04/asia/deepfake-cfo-scam-hong-kong-intl-hnk)
- [Fortune: A deepfake 'CFO' tricked British design firm Arup in $25 million fraud](https://fortune.com/europe/2024/05/17/arup-deepfake-fraud-scam-victim-hong-kong-25-million-cfo/)
- [CFO Dive: Scammers siphon $25M via AI deepfake CFO](https://www.cfodive.com/news/scammers-siphon-25m-engineering-firm-arup-deepfake-cfo-ai/716501/)

#### Voice Cloning Attacks
- [Fortune: Ferrari exec foils deepfake attempt with a book question](https://fortune.com/2024/07/27/ferrari-deepfake-attempt-scammer-security-question-ceo-benedetto-vigna-cybersecurity-ai/)
- [MIT Sloan: How Ferrari Hit the Brakes on a Deepfake CEO](https://sloanreview.mit.edu/article/how-ferrari-hit-the-brakes-on-a-deepfake-ceo/)
- [Right-Hand: State of Deep Fake Vishing Attacks 2025](https://right-hand.ai/blog/deep-fake-vishing-attacks-2025/)
- [Brightside AI: Deepfake CEO Fraud — the $50M Voice Cloning Threat](https://www.brside.com/blog/deepfake-ceo-fraud-50m-voice-cloning-threat-cfos)

#### KnowBe4 North Korean Deepfake Employee
- [KnowBe4: How a North Korean Fake IT Worker Tried to Infiltrate Us](https://blog.knowbe4.com/how-a-north-korean-fake-it-worker-tried-to-infiltrate-us)
- [CyberScoop: KnowBe4 hired a fake IT worker from North Korea](https://cyberscoop.com/cyber-firm-knowbe4-hired-a-fake-it-worker-from-north-korea/)
- [iProov: The KnowBe4 Deepfake Wake-Up Call](https://www.iproov.com/blog/knowbe4-deepfake-wake-up-call-remote-hiring-security)

#### Deepfake-as-a-Service
- [Cyble: Deepfake-as-a-Service Exploded in 2025](https://cyble.com/knowledge-hub/deepfake-as-a-service-exploded-in-2025/)
- [Dark Reading: Deepfake-Generating Apps Explode](https://www.darkreading.com/threat-intelligence/deepfake-apps-explode-multimillion-dollar-corporate-heists)
- [Kaspersky: Deepfake market analysis](https://www.kaspersky.com/blog/deepfake-darknet-market/48112/)
- [Group-IB: From Deepfakes to Dark LLMs](https://www.group-ib.com/blog/ai-cybercrime-usecases/)

### Detection Accuracy Research
- [ScienceDirect: Human performance in detecting deepfakes (meta-analysis of 67 studies)](https://www.sciencedirect.com/science/article/pii/S2451958824001714)
- [Ceartas: Measuring Deepfake Detection Accuracy 2025](https://blog.ceartas.io/p/deepfake-detection-accuracy)
- [TTMS: Universal Detector Achieves 98% Accuracy](https://ttms.com/deepfake-detection-breakthrough-universal-detector-achieves-98-accuracy/)
- [iProov 2025: Only 0.1% of participants identified all fakes](https://www.brightdefense.com/resources/deepfake-statistics/)
- [PyData Global 2024: Off-the-shelf HuggingFace models for audio deepfake detection](https://global2024.pydata.org/cfp/talk/LJPSKA/)

### Deepfake Statistics & Trends
- [Keepnet: Deepfake Statistics & Trends 2026](https://keepnetlabs.com/blog/deepfake-statistics-and-trends)
- [DeepStrike: Deepfake Statistics 2025](https://deepstrike.io/blog/deepfake-statistics-2025)
- [Bright Defense: 150+ Deepfake Statistics (March 2026)](https://www.brightdefense.com/resources/deepfake-statistics/)
- [Fortune: 2026 will be the year you get fooled by a deepfake](https://fortune.com/2025/12/27/2026-deepfakes-outlook-forecast/)
- [Eftsure: Deepfake statistics 2025](https://www.eftsure.com/statistics/deepfake-statistics/)

### Broader AI Threat Landscape
- [Elnion: Analysis of Reddit CyberSecurity Discussions 2026](https://elnion.com/2026/01/27/from-phishing-to-ai-chaos-what-my-analysis-of-all-reddit-cybersecurity-discussions-so-far-in-2026-revealed/)
- [Norton: Top 5 Ways Scammers Used AI and Deepfakes in 2025](https://us.norton.com/blog/online-scams/top-5-ai-and-deepfakes-2025)
- [Euronews: How deepfake scams are reaching record levels](https://www.euronews.com/my-europe/2026/02/23/how-deepfake-scams-are-reaching-record-levels-by-targeting-social-media-users)
- [World Economic Forum: Deepfakes are here to stay](https://www.weforum.org/stories/2025/01/deepfakes-different-threat-than-expected/)
- [McAfee: World's Most Deepfaked Celebrities](https://www.mcafee.com/blogs/internet-security/the-stars-scammers-love-most-mcafee-reveals-worlds-most-deepfaked-celebs/)

### Regulation
- [EU AI Act Article 50: Transparency obligations](https://artificialintelligenceact.eu/article/50/)
- [TechPolicy.Press: What the EU's New AI Code of Practice Means for Labeling Deepfakes](https://www.techpolicy.press/what-the-eus-new-ai-code-of-practice-means-for-labeling-deepfakes/)
- [Reality Defender: EU AI Act Deepfake Rules](https://www.realitydefender.com/insights/which-companies-must-comply-with-the-eu-ai-acts-deepfake-requirements)
- [Jones Day: European Commission Draft Code of Practice on AI Labelling](https://www.jonesday.com/en/insights/2026/01/european-commission-publishes-draft-code-of-practice-on-ai-labelling-and-transparency)
