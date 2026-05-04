# Research — Similar Projects & Landscape Analysis

> **Date:** 2026-04-20
> **Purpose:** Understand the existing deepfake detection landscape and position DeepFakeGuard relative to other tools.

---

## Open-Source Tools

### 1. Deepfake-o-Meter (University at Buffalo)

| Detail | Info |
|--------|------|
| **Developer** | UB Media Forensics Lab (Prof. Siwei Lyu) |
| **Type** | Open-source web platform |
| **URL** | [zinc.cse.buffalo.edu/ubmdfl/deep-o-meter](https://zinc.cse.buffalo.edu/ubmdfl/deep-o-meter/landing_page) |
| **GitHub** | Not fully open-sourced (web service with paper) |
| **Media types** | Images, video |
| **Detection methods** | 18 detection algorithms aggregated |
| **Users** | 445+ across 98 countries |
| **Paper** | [arXiv:2404.13146](https://arxiv.org/abs/2404.13146) |

**What it does:** Upload an image or video, get analyzed by multiple detection algorithms simultaneously. Aggregates scores from different methods into a unified report.

**Strengths:**
- Multiple algorithms running in parallel — diverse detection approaches
- Academic credibility (published research)
- Free and publicly accessible

**Weaknesses:**
- No API — only web upload (not developer-friendly)
- No audio deepfake detection
- No plain-English explanations — outputs raw scores
- No C2PA/content provenance checking
- Not designed for integration into security workflows

**How we compare:** DeepFakeGuard provides a REST API (programmable), covers audio + images, generates plain-English explanations, and checks C2PA provenance. We trade breadth of detection algorithms for depth of explainability and developer ergonomics.

---

### 2. DeepSafe

| Detail | Info |
|--------|------|
| **Developer** | Siddharth K Sah |
| **Type** | Open-source (GitHub) |
| **GitHub** | [github.com/siddharthksah/DeepSafe](https://github.com/siddharthksah/DeepSafe) |
| **Media types** | Images, video |
| **Tech** | Python, PyTorch |
| **Overview** | [Medium article](https://siddharthksah.medium.com/deepsafe-open-source-deepfake-detection-42f1c18f9500) |

**What it does:** Enterprise-grade modular detection platform. Designed as a pipeline where different detection modules can be plugged in.

**Strengths:**
- Modular architecture — pluggable detectors
- Open-source and actively maintained
- Enterprise-focused design patterns

**Weaknesses:**
- Primarily image/video focused — no audio detection
- No AI-powered explanations
- No content provenance checking
- Limited documentation

**How we compare:** DeepFakeGuard has a similar modular philosophy but includes audio detection, AI explanations via Claude, and C2PA provenance — features DeepSafe doesn't offer.

---

### 3. Deepware Scanner

| Detail | Info |
|--------|------|
| **Developer** | Deepware Neurons |
| **Type** | Open-source desktop app |
| **GitHub** | [github.com/deepware-neurons/deepware-scanner](https://github.com/deepware-neurons/deepware-scanner) |
| **Media types** | Video |

**What it does:** Desktop application for scanning videos for deepfake manipulation. Uses multiple detection models.

**Strengths:**
- Easy-to-use desktop GUI
- Multiple model ensemble
- Open-source

**Weaknesses:**
- Video only — no audio or image detection
- Desktop-only — no API or web interface
- Not designed for enterprise/programmatic use
- Limited to facial manipulation detection

**How we compare:** DeepFakeGuard is API-first (no desktop install needed), covers audio + images, and is designed for integration into security toolchains.

---

### 4. DeepfakeBench (SCLBD / Chinese Academy of Sciences)

| Detail | Info |
|--------|------|
| **Developer** | Shengnan Liu et al. |
| **Type** | Open-source evaluation framework |
| **GitHub** | [github.com/SCLBD/DeepfakeBench](https://github.com/SCLBD/DeepfakeBench) |
| **Paper** | NeurIPS 2023 |
| **Media types** | Images, video |
| **Scope** | 9 datasets, 36 detection methods unified |

**What it does:** Not a detection tool per se — it's a unified benchmarking framework for evaluating and comparing deepfake detection methods. Standardizes preprocessing, training, and evaluation.

**Strengths:**
- Most comprehensive evaluation framework available
- 36 detection methods with pretrained weights
- Standardized cross-dataset evaluation
- Academic gold standard for benchmarking

**Weaknesses:**
- Research tool, not production-ready
- No API, no user interface
- No audio detection
- Requires significant ML expertise to use

**How we compare:** DeepfakeBench is what you'd use to evaluate your model. DeepFakeGuard is what you'd use to deploy one. They're complementary — we could use DeepfakeBench's pretrained models in our pipeline.

---

### 5. DFDC — Facebook/Meta Deepfake Detection Challenge

| Detail | Info |
|--------|------|
| **Developer** | Meta (Facebook) |
| **Type** | Open-source datasets + baselines |
| **GitHub** | [github.com/facebookresearch/dfdc](https://github.com/facebookresearch/dfdc) |
| **Media types** | Video |
| **Year** | 2020 |

**What it does:** Facebook's challenge released a large dataset of real and fake videos plus baseline detection models. The code provides training pipelines for video-level deepfake classification.

**Strengths:**
- Large-scale dataset (100K+ videos)
- Industry-backed with significant resources
- Baseline models included

**Weaknesses:**
- Challenge is over — not actively maintained
- Video-only
- Dataset is aging (2020-era deepfakes, not current generators)
- No API or deployment tooling

**How we compare:** DFDC is a dataset/resource, not a deployable tool. DeepFakeGuard uses more recent models trained on current-generation deepfakes (DF40 includes MidJourney 6, Stable Diffusion, etc.).

---

## Commercial / Enterprise Tools

### 6. Reality Defender

| Detail | Info |
|--------|------|
| **Developer** | Reality Defender Inc. |
| **Type** | Commercial SaaS |
| **URL** | [realitydefender.com](https://realitydefender.com) |
| **Media types** | Text, images, audio, video |
| **Clients** | Enterprises, governments, financial institutions |

**What it does:** Enterprise deepfake detection platform with multi-modal scanning (text, image, audio, video). Provides real-time analysis, probability scoring, and REST API access.

**Strengths:**
- Most comprehensive coverage (4 media types)
- SOC 2 compliant, enterprise-ready
- Real-time scanning
- Batch processing at scale
- Used in 2024 US election cycle
- Dashboard and reporting

**Weaknesses:**
- Closed-source / proprietary
- Enterprise pricing (not accessible for individuals/small teams)
- No explainability — outputs scores, not explanations
- No content provenance checking

**How we compare:** Reality Defender is the enterprise incumbent. DeepFakeGuard is open-source, free, and focused on explainability (plain-English reports). We target developers and small security teams who can't afford enterprise pricing.

---

### 7. Sensity AI

| Detail | Info |
|--------|------|
| **Developer** | Sensity AI (formerly DeepTrace) |
| **Type** | Commercial API |
| **URL** | [sensity.ai](https://sensity.ai) |
| **Media types** | Images, video |

**What it does:** AI-powered visual threat intelligence platform. Detects deepfakes, synthetic identities, and manipulated media via API.

**Strengths:**
- Specialized in visual threat intelligence
- API-first design
- Focus on identity fraud use cases
- Threat intelligence feeds

**Weaknesses:**
- No audio detection
- Closed-source, commercial pricing
- No explainability layer
- No content provenance

**How we compare:** DeepFakeGuard adds audio detection, AI explanations, and C2PA provenance — none of which Sensity offers.

---

### 8. Microsoft Video Authenticator / Content Credentials

| Detail | Info |
|--------|------|
| **Developer** | Microsoft |
| **Type** | Hybrid (tool + standard) |
| **Media types** | Images, video |
| **Initiative** | Content Credentials (C2PA coalition) |

**What it does:** Microsoft's Video Authenticator analyzes photos and videos for deepfake artifacts. Microsoft is also a founding member of the C2PA coalition for content provenance.

**Strengths:**
- Backed by Microsoft's research infrastructure
- Integrated with the C2PA standard (Microsoft is a founding member)
- Enterprise-grade

**Weaknesses:**
- Not publicly available as an API (limited access)
- Part of a broader ecosystem, not standalone
- No audio detection
- No open-source version

**How we compare:** We implement the same C2PA standard (Microsoft helped create) in an open-source, self-hosted tool. Our C2PA viewer gives anyone the ability to check content credentials, not just Microsoft partners.

---

### 9. Intel FakeCatcher

| Detail | Info |
|--------|------|
| **Developer** | Intel |
| **Type** | Commercial / research |
| **Media types** | Video |

**What it does:** Deepfake detection technology that analyzes blood flow in video (photoplethysmography). Detects real vs. fake by looking for authentic physiological signals in faces.

**Strengths:**
- Novel detection approach (physiological signals, not pixel artifacts)
- Harder to fool than pixel-based detectors
- Real-time capable on Intel hardware

**Weaknesses:**
- Requires video with visible face — doesn't work on audio or images
- Tied to Intel hardware
- Not publicly available as open-source
- Specialized approach — limited to one detection vector

**How we compare:** FakeCatcher uses a clever physiological approach but is limited to video. DeepFakeGuard covers audio and images with multiple complementary signals (spectral, pitch, breathing, FFT, GAN artifacts, metadata).

---

## Research Frameworks & Benchmarks (Used by DeepFakeGuard)

| Resource | What it provides | How we use it |
|----------|-----------------|---------------|
| **ASVspoof 5** (2024) | Gold-standard voice anti-spoofing benchmark | Evaluating our audio model |
| **DF40** (NeurIPS 2024) | 40 deepfake techniques benchmark | Evaluating our image model |
| **MLAAD v9** (Jan 2026) | 678h synthetic speech, 51 languages | Testing multilingual generalization |
| **DeepfakeBench** (NeurIPS 2023) | Unified evaluation framework | Cross-dataset evaluation |
| **MITRE ATLAS** | AI threat taxonomy (16 tactics, 84 techniques) | Mapping our detections to standard threat IDs |
| **C2PA Specification** | Content provenance standard (Adobe, Google, Microsoft, OpenAI) | Our Module 4 implementation |

---

## Positioning Summary

```
                    Open Source  │  Commercial
                 ┌───────────────┼───────────────────┐
   Audio + Image │ DeepFakeGuard │ Reality Defender   │
                 │               │ Sensity AI         │
                 ├───────────────┼───────────────────┤
   Video Only    │ Deepware      │ Intel FakeCatcher  │
                 │ Deepfake-o-   │ Microsoft Video    │
                 │   Meter       │   Authenticator    │
                 ├───────────────┼───────────────────┤
   Eval Only     │ DeepfakeBench │                    │
                 │ DFDC (Meta)   │                    │
                 └───────────────┴───────────────────┘
```

**DeepFakeGuard's unique combination:**
1. **Audio + Image** detection in one toolkit
2. **AI-powered explanations** (not just scores) — via Claude API
3. **C2PA Content Credentials** checking — ahead of EU AI Act compliance
4. **Open-source** and self-hosted — no vendor lock-in
5. **REST API first** — designed for developer integration
6. **MITRE ATLAS mapping** — ties into security team workflows

No other open-source tool combines all six. The closest (Deepfake-o-Meter) is web-only with no API, no audio detection, no explanations, and no provenance checking.
