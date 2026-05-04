# Spec Index — DeepFakeGuard

> All spec documents for the project. Read these before writing code.

## Documents

| Document | Purpose | Status |
|----------|---------|--------|
| [PRD.md](PRD.md) | Product Requirements — user stories, functional/non-functional requirements, success metrics | Draft |
| [TECH_SPEC.md](TECH_SPEC.md) | Technical Specification — architecture, data models, tech stack, project structure, ML strategy | Draft |
| [API_SPEC.md](API_SPEC.md) | API Specification — all endpoints, request/response schemas, error codes, severity logic | Draft |
| [RESEARCH.md](RESEARCH.md) | Landscape analysis — similar open-source & commercial tools, positioning, benchmarks | Complete |

## Spec-Driven Development Workflow

1. **Read the spec** — Before starting a module, read the relevant sections in all three documents.
2. **Implement to spec** — Write code that satisfies the requirements and matches the API contracts.
3. **Validate against spec** — After implementation, verify:
   - All user stories for the module are satisfied
   - API response matches the documented schema
   - Error codes match the specification
   - Non-functional requirements are met (latency, file size limits)
4. **Update the spec** — If reality requires a spec change, update the document *before* changing the code. Commit the spec change with the code change.

## Module → Spec Mapping

| Module | PRD Sections | TECH_SPEC Sections | API_SPEC Sections |
|--------|-------------|-------------------|-------------------|
| 1. Voice Detector | US-1.1 to US-1.4, FR-1, FR-2 | §2, §4.4, §6.1 | §2.2 |
| 2. Image Detector | US-2.1 to US-2.3, FR-3, FR-4 | §2, §4.5, §6.2 | §2.3 |
| 3. AI Explainer | US-3.1 to US-3.4, FR-5 to FR-8, FR-11 | §4.1, §4.3, §7 | §1.3, §3, §4 |
| 4. C2PA Viewer | US-4.1 to US-4.3, FR-9, FR-10 | §4.6 | §2.4 |
| 5. Dashboard | US-5.1 to US-5.4, FR-12 to FR-15 | §3 | §2.1, §2.5, §2.6 |

## Build Order

```
Phase 1: Shared skeleton (FastAPI app, config, DB, project structure)
Phase 2: Module 1 (Audio) + Module 2 (Image) — can run in parallel
Phase 3: Module 3 (Explainer) — depends on Modules 1 & 2
Phase 4: Module 4 (C2PA) — independent
Phase 5: Module 5 (Dashboard) — integrates everything
```
