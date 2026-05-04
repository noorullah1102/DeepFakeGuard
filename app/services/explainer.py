"""AI Threat Explainer — generates plain-English explanations using Claude API."""

from app.config import settings

EXPLAIN_PROMPT = """You are a cybersecurity analyst explaining deepfake detection results to a non-technical audience.

Analyze the following detection result and provide:

1. **What was detected** — specific artifacts and anomalies found
2. **Why it matters** — severity, attack type, and real-world context
3. **Confidence assessment** — what the system is sure about vs uncertain
4. **Recommended action** — concrete next step for the user

Detection result:
- Media type: {media_type}
- Verdict: {verdict}
- Confidence: {confidence}
- Severity: {severity}
- Analysis details: {analysis}

Provide a clear, concise explanation in 3-5 sentences. Be specific about what artifacts were found. Use plain English that a finance team or security analyst could act on.

Do not include markdown headers or bullet points — write as a single flowing paragraph.
"""

FALLBACK_EXPLANATIONS = {
    ("synthetic", "critical"): "This audio exhibits multiple strong indicators of AI generation. The combination of spectral artifacts, unnatural pitch stability, and absent breathing patterns is consistent with voice cloning or text-to-speech technology. This is very likely a synthetic voice — do not trust or act on any instructions in this recording. Verify the speaker through a separate, known channel immediately.",
    ("synthetic", "high"): "This audio shows significant signs of being AI-generated. Key indicators include unnatural pitch consistency and missing breathing patterns typical of synthetic speech. We recommend verifying the speaker's identity through a separate channel before taking any action.",
    ("synthetic", "medium"): "This audio has some characteristics associated with AI-generated speech, though the evidence is not conclusive. Further verification of the speaker's identity is recommended.",
    ("manipulated", "critical"): "This image shows strong evidence of AI generation or heavy manipulation. GAN-generated artifacts, abnormally perfect facial symmetry, and stripped metadata all point to a synthetic image. This should not be used for identity verification under any circumstances.",
    ("manipulated", "high"): "This image appears to be AI-generated or significantly manipulated. Key indicators include frequency-domain anomalies and metadata inconsistencies. Request alternative verification before trusting this image.",
    ("manipulated", "medium"): "This image has some characteristics associated with AI manipulation, though the evidence is not conclusive. Additional verification is recommended.",
    ("real", "low"): "No significant indicators of AI generation or manipulation were detected. The media appears to be authentic based on the analysis performed.",
}

ACTION_MAP = {
    ("synthetic", "critical"): "Do not act on any instructions from this audio. Verify the speaker's identity through a known, separate channel. Report to your security team immediately.",
    ("synthetic", "high"): "Do not act on instructions from this audio without verifying the speaker's identity through a separate, trusted channel.",
    ("synthetic", "medium"): "Verify the speaker's identity through an alternative channel before taking action on any requests.",
    ("synthetic", "low"): "Audio appears genuine, but always verify sensitive requests through established protocols.",
    ("manipulated", "critical"): "Do not use this image for identity verification. Request a live video verification with liveness detection. Report to security team.",
    ("manipulated", "high"): "Do not use this image for identity verification. Request alternative verification methods.",
    ("manipulated", "medium"): "Treat this image with caution. Request additional verification before using for sensitive purposes.",
    ("manipulated", "low"): "Image appears genuine, but follow standard verification procedures for sensitive use cases.",
    ("real", "low"): "No immediate action required. Follow standard security protocols.",
}


def generate_explanation(detection_result: dict) -> tuple[str, str]:
    """Generate AI explanation and recommended action for a detection result.

    Returns (explanation, action).
    Tries Claude API first, falls back to pre-written templates.
    """
    verdict = detection_result.get("verdict", "real")
    confidence = detection_result.get("confidence", 0.0)
    severity = detection_result.get("severity", "low")
    media_type = detection_result.get("media_type", "unknown")
    analysis = detection_result.get("analysis", {})

    # Try Claude API
    explanation = _call_claude(verdict, confidence, severity, media_type, analysis)
    if explanation:
        action = ACTION_MAP.get((verdict, severity), "Follow standard verification procedures.")
        return explanation, action

    # Fallback to templates
    key = (verdict, severity)
    explanation = FALLBACK_EXPLANATIONS.get(key, f"Detection result: {verdict} with {confidence:.0%} confidence.")
    action = ACTION_MAP.get(key, "Follow standard verification procedures.")

    return explanation, action


def _call_claude(
    verdict: str, confidence: float, severity: str, media_type: str, analysis: dict
) -> str | None:
    """Call Claude API for explanation. Returns None on failure."""
    if not settings.anthropic_api_key:
        return None

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        prompt = EXPLAIN_PROMPT.format(
            media_type=media_type,
            verdict=verdict,
            confidence=f"{confidence:.0%}",
            severity=severity,
            analysis=analysis,
        )

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )

        return response.content[0].text.strip()

    except Exception as e:
        print(f"Warning: Claude API call failed: {e}")
        return None
