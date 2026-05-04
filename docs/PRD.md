# Product Requirements Document — DeepFakeGuard

> **Version:** 1.0
> **Date:** 2026-04-20
> **Status:** Draft

## 1. Problem Statement

Deepfakes are a billion-dollar fraud vector. Humans detect them 55% of the time — barely better than a coin flip. Creation tools cost $10; detection tools are locked in research labs. Security teams, developers, and analysts need a practical, explainable detection tool.

## 2. Product Vision

An open-source Python toolkit that detects AI-generated voices and manipulated images, explains findings in plain English, and checks media provenance — giving defenders an actual edge over guessing.

## 3. Target Users

| User | Need |
|------|------|
| Security analysts | Detect deepfakes in incident response |
| Developers | Integrate deepfake detection into apps via API |
| Hiring managers / recruiters | Evaluate candidate's ML and engineering skills |

## 4. User Stories

### Module 1 — Voice Deepfake Detector

- **US-1.1** As a security analyst, I want to upload an audio file and get a real/synthetic verdict so I can decide whether to trust it.
- **US-1.2** As a security analyst, I want to see a confidence score so I know how reliable the verdict is.
- **US-1.3** As a security analyst, I want to see which audio artifacts triggered the detection (spectral anomalies, missing breathing, pitch consistency) so I can validate the result.
- **US-1.4** As a developer, I want to call a REST endpoint (`POST /api/v1/detect/audio`) and get structured JSON so I can integrate detection into my own tools.

### Module 2 — Image Deepfake Detector

- **US-2.1** As a security analyst, I want to upload an image and get a real/manipulated verdict so I can decide whether to trust it.
- **US-2.2** As a security analyst, I want to see which visual artifacts were detected (GAN patterns, lighting inconsistencies, EXIF issues) so I can validate the result.
- **US-2.3** As a developer, I want to call a REST endpoint (`POST /api/v1/detect/image`) and get structured JSON so I can integrate detection into my own tools.

### Module 3 — AI Threat Explainer

- **US-3.1** As a non-technical user, I want a plain-English explanation of why media was flagged so I can understand and act on it.
- **US-3.2** As a security analyst, I want a severity rating (low/medium/high/critical) so I can prioritize my response.
- **US-3.3** As a security analyst, I want recommended actions so I know what to do next.
- **US-3.4** As a security analyst, I want MITRE ATLAS mapping so I can log the threat type in our incident system.

### Module 4 — C2PA Content Credentials Viewer

- **US-4.1** As a security analyst, I want to check if media has C2PA Content Credentials so I can verify its provenance.
- **US-4.2** As a compliance officer, I want to see the full credential chain (creator, tool, edit history) so I can audit media origins.
- **US-4.3** As a developer, I want to call a REST endpoint (`POST /api/v1/provenance`) and get credential data so I can automate checks.

### Module 5 — Dashboard & Integration

- **US-5.1** As a user, I want a web UI where I can drag-and-drop files for analysis so I don't need to use the API directly.
- **US-5.2** As a user, I want to see my scan history so I can track what I've analyzed.
- **US-5.3** As a user, I want to see detection trends over time so I can spot patterns.
- **US-5.4** As a developer, I want Swagger docs so I can understand the API without reading source code.

## 5. Functional Requirements

| ID | Requirement | Module | Priority |
|----|-------------|--------|----------|
| FR-1 | Accept `.wav`, `.mp3`, `.flac` audio uploads | 1 | P0 |
| FR-2 | Return verdict, confidence, and artifact breakdown for audio | 1 | P0 |
| FR-3 | Accept `.jpg`, `.png`, `.webp` image uploads | 2 | P0 |
| FR-4 | Return verdict, confidence, and artifact breakdown for images | 2 | P0 |
| FR-5 | Generate plain-English threat explanations via Claude API | 3 | P0 |
| FR-6 | Assign severity ratings (low/medium/high/critical) | 3 | P0 |
| FR-7 | Provide recommended actions per detection | 3 | P1 |
| FR-8 | Map detections to MITRE ATLAS techniques | 3 | P1 |
| FR-9 | Parse and display C2PA Content Credentials | 4 | P0 |
| FR-10 | Handle three C2PA states: present, absent, tampered | 4 | P0 |
| FR-11 | Store scan history in SQLite | 3 | P1 |
| FR-12 | Serve REST API with Swagger docs | 5 | P0 |
| FR-13 | Web dashboard with drag-and-drop upload | 5 | P1 |
| FR-14 | Scan history table with filtering | 5 | P1 |
| FR-15 | Detection trends chart | 5 | P2 |

## 6. Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | Audio detection latency | < 10s per file (under 60s audio) |
| NFR-2 | Image detection latency | < 5s per image |
| NFR-3 | API uptime | 99%+ during local dev |
| NFR-4 | Max audio file size | 50 MB |
| NFR-5 | Max image file size | 20 MB |
| NFR-6 | Supported Python | 3.11+ |
| NFR-7 | Code test coverage | > 70% for each module |
| NFR-8 | All API responses JSON | Structured, consistent schema |

## 7. Out of Scope

- Video deepfake detection (future work)
- Real-time stream monitoring
- User authentication / multi-user
- Cloud deployment (MVP is local-only)
- Mobile app
- Training models from scratch (using pre-trained / fine-tuned)

## 8. Success Metrics

| Metric | Target |
|--------|--------|
| Audio detection EER | Competitive with ASVspoof 5 baselines |
| Image detection AUC | > 0.85 on DF40 test set |
| API response schema | Consistent across all endpoints |
| Module independence | Each module runs and demos standalone |
| Portfolio readiness | README with screenshots + demo video |
