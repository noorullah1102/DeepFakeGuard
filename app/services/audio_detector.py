"""Audio deepfake detection service."""

import uuid

import numpy as np

from app.config import settings
from app.utils.audio_features import analyze_artifacts, extract_features, load_audio


class AudioDetector:
    """Detects AI-generated / synthetic audio using feature analysis + ML model."""

    def __init__(self):
        self.model = None
        self.processor = None
        self._model_loaded = False

    def load_model(self):
        """Load the Wav2Vec2-based deepfake audio detection model from HuggingFace."""
        try:
            from transformers import AutoFeatureExtractor, AutoModelForAudioClassification

            model_name = settings.model_audio
            self.processor = AutoFeatureExtractor.from_pretrained(model_name)
            self.model = AutoModelForAudioClassification.from_pretrained(model_name)
            self._model_loaded = True
        except Exception as e:
            print(f"Warning: Could not load audio model: {e}")
            print("Audio detection will use rule-based analysis only.")
            self._model_loaded = False

    @property
    def is_loaded(self) -> bool:
        return self._model_loaded

    def detect(self, audio_bytes: bytes, filename: str = "") -> dict:
        """Run full audio deepfake detection pipeline.

        Returns a DetectionResponse-compatible dict.
        """
        # Load and extract features
        waveform, sr = load_audio(audio_bytes, sr=16000)
        features = extract_features(waveform, sr)
        artifacts = analyze_artifacts(features)

        # Model inference (if loaded)
        model_verdict = None
        model_confidence = None

        if self._model_loaded:
            model_verdict, model_confidence = self._predict_model(waveform, sr)

        # Combine rule-based + model verdicts
        verdict, confidence, severity = self._compute_verdict(
            artifacts, model_verdict, model_confidence
        )

        mitre_atlas = "AML.T0048"

        return {
            "id": str(uuid.uuid4()),
            "verdict": verdict,
            "confidence": round(confidence, 2),
            "media_type": "audio",
            "analysis": artifacts,
            "severity": severity,
            "mitre_atlas": mitre_atlas,
            "filename": filename,
        }

    def _predict_model(self, waveform: np.ndarray, sr: int) -> tuple[str, float]:
        """Run ML model prediction on audio waveform."""
        import torch

        inputs = self.processor(
            waveform, sampling_rate=sr, return_tensors="pt", padding=True
        )

        with torch.no_grad():
            logits = self.model(**inputs).logits

        probs = torch.softmax(logits, dim=-1)
        predicted_class = torch.argmax(probs, dim=-1).item()
        confidence = probs[0][predicted_class].item()

        # Model label mapping: garystafford uses {0: 'real', 1: 'fake'}
        # Adjust if a different model is configured
        label = "real" if predicted_class == 0 else "synthetic"

        return label, confidence

    def _compute_verdict(
        self,
        artifacts: dict,
        model_verdict: str | None,
        model_confidence: float | None,
    ) -> tuple[str, float, str]:
        """Combine rule-based and model signals into final verdict."""
        # Count suspicious signals from rule-based analysis
        suspicious_signals = 0
        if artifacts["spectral_artifacts"]:
            suspicious_signals += 1
        if artifacts["pitch_consistency"] < 0.5:
            suspicious_signals += 1
        if artifacts["breathing_patterns"] == "absent":
            suspicious_signals += 1
        if artifacts["background_noise"] == "unnaturally_uniform":
            suspicious_signals += 1

        # If model is loaded, weigh model heavily (lowered threshold to 0.4
        # for better recall on modern TTS)
        if model_verdict and model_confidence is not None:
            if model_verdict == "synthetic" and model_confidence > 0.4:
                combined_confidence = model_confidence * 0.8 + min(suspicious_signals / 4, 1.0) * 0.2
                verdict = "synthetic"
            elif model_verdict == "real" and model_confidence > 0.4:
                combined_confidence = model_confidence * 0.8 + (1 - min(suspicious_signals / 4, 1.0)) * 0.2
                verdict = "real"
            else:
                # Low model confidence — fall back to rule-based
                combined_confidence = min(suspicious_signals / 4, 1.0)
                verdict = "synthetic" if suspicious_signals >= 2 else "real"
        else:
            # Rule-based only
            combined_confidence = min(suspicious_signals / 4, 1.0)
            verdict = "synthetic" if suspicious_signals >= 2 else "real"

        # Severity
        if combined_confidence >= 0.85 and suspicious_signals >= 3:
            severity = "critical"
        elif combined_confidence >= 0.7 and suspicious_signals >= 2:
            severity = "high"
        elif combined_confidence >= 0.5:
            severity = "medium"
        else:
            severity = "low"

        # Adjustments
        if artifacts["breathing_patterns"] == "absent" and severity in ("medium", "low"):
            severity = "high"

        return verdict, combined_confidence, severity


# Singleton instance
audio_detector = AudioDetector()
