"""Image deepfake detection service with dual-model ensemble."""

import uuid

from app.config import settings
from app.utils.image_features import (
    check_metadata_integrity,
    extract_features,
    load_image,
    validate_image_file,
)


class ImageDetector:
    """Detects AI-generated / manipulated images using feature analysis + ML ensemble."""

    def __init__(self):
        self.model = None
        self.processor = None
        self.model_ensemble = None
        self.processor_ensemble = None
        self._model_loaded = False
        self._ensemble_loaded = False

    def load_model(self):
        """Load both image detection models from HuggingFace."""
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            # Primary model: CommunityForensics ViT
            try:
                from transformers import AutoModelForImageClassification

                self.model = AutoModelForImageClassification.from_pretrained(
                    settings.model_image
                )
                self._model_loaded = True
                print(f"Loaded primary image model: {settings.model_image}")
            except Exception as e:
                print(f"Warning: Could not load primary image model: {e}")
                self._model_loaded = False

            # Ensemble model: prithivMLmods SigLIP
            try:
                from transformers import AutoImageProcessor, AutoModelForImageClassification

                self.processor_ensemble = AutoImageProcessor.from_pretrained(
                    settings.model_image_ensemble
                )
                self.model_ensemble = AutoModelForImageClassification.from_pretrained(
                    settings.model_image_ensemble
                )
                self._ensemble_loaded = True
                print(f"Loaded ensemble image model: {settings.model_image_ensemble}")
            except Exception as e:
                print(f"Warning: Could not load ensemble image model: {e}")
                self._ensemble_loaded = False

        if not self._model_loaded and not self._ensemble_loaded:
            print("Image detection will use rule-based analysis only.")

    @property
    def is_loaded(self) -> bool:
        return self._model_loaded or self._ensemble_loaded

    def detect(self, image_bytes: bytes, filename: str = "") -> dict:
        """Run full image deepfake detection pipeline."""
        image = load_image(image_bytes)
        metadata_status = check_metadata_integrity(image_bytes)
        features = extract_features(image)
        features["metadata_integrity"] = metadata_status

        model_verdict = None
        model_confidence = None

        if self._model_loaded or self._ensemble_loaded:
            model_verdict, model_confidence = self._predict_ensemble(image_bytes)

        verdict, confidence, severity = self._compute_verdict(
            features, model_verdict, model_confidence
        )

        mitre_atlas = "AML.T0048.002"

        return {
            "id": str(uuid.uuid4()),
            "verdict": verdict,
            "confidence": round(confidence, 2),
            "media_type": "image",
            "analysis": features,
            "severity": severity,
            "mitre_atlas": mitre_atlas,
            "filename": filename,
        }

    def _predict_ensemble(self, image_bytes: bytes) -> tuple[str, float]:
        """Run both models and combine their predictions.

        When models disagree (one says fake, other says real), it's a signal
        that the image is likely AI-generated — real photos rarely cause
        disagreement between architectures.
        """
        import torch
        from PIL import Image
        import io

        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        fake_probs = []
        weights = []

        # --- CommunityForensics ViT (50% weight) ---
        if self._model_loaded:
            try:
                import torchvision.transforms as T

                transform = T.Compose([
                    T.Resize((384, 384), interpolation=T.InterpolationMode.BICUBIC),
                    T.ToTensor(),
                    T.Normalize(
                        mean=[0.4815, 0.4578, 0.4082],
                        std=[0.2686, 0.2613, 0.2758],
                    ),
                ])
                pixel_values = transform(image).unsqueeze(0)
                with torch.no_grad():
                    logits = self.model(pixel_values=pixel_values).logits
                probs = torch.softmax(logits, dim=-1)
                fake_prob = probs[0][1].item()
                fake_probs.append(fake_prob)
                weights.append(0.5)
            except Exception as e:
                print(f"CommunityForensics inference failed: {e}")

        # --- prithivMLmods SigLIP (50% weight) ---
        if self._ensemble_loaded:
            try:
                inputs = self.processor_ensemble(images=image, return_tensors="pt")
                with torch.no_grad():
                    logits = self.model_ensemble(**inputs).logits
                probs = torch.softmax(logits, dim=-1)
                # id2label={0: 'Fake', 1: 'Real'}
                fake_prob = probs[0][0].item()
                fake_probs.append(fake_prob)
                weights.append(0.5)
            except Exception as e:
                print(f"prithivMLmods inference failed: {e}")

        if not fake_probs:
            return None, None

        # Weighted average
        total_weight = sum(weights)
        combined_fake = sum(p * w for p, w in zip(fake_probs, weights)) / total_weight

        # Disagreement bonus: if models disagree (one >0.5 fake, other <0.5 fake),
        # it's suspicious — boost fake probability. Real images rarely cause this.
        if len(fake_probs) == 2:
            disagreement = abs(fake_probs[0] - fake_probs[1])
            if fake_probs[0] > 0.5 and fake_probs[1] < 0.5:
                combined_fake = max(combined_fake, max(fake_probs) * 0.7)
            elif fake_probs[1] > 0.5 and fake_probs[0] < 0.5:
                combined_fake = max(combined_fake, max(fake_probs) * 0.7)

        label = "manipulated" if combined_fake > 0.5 else "real"
        confidence = max(combined_fake, 1 - combined_fake)

        return label, confidence

    def _compute_verdict(
        self,
        features: dict,
        model_verdict: str | None,
        model_confidence: float | None,
    ) -> tuple[str, float, str]:
        """Combine rule-based and model signals into final verdict."""
        suspicious_signals = 0
        if features.get("gan_artifacts"):
            suspicious_signals += 1
        if features.get("facial_symmetry", 0) > 0.95:
            suspicious_signals += 1
        if features.get("lighting_consistency", 1.0) < 0.65:
            suspicious_signals += 1
        if features.get("metadata_integrity") == "exif_stripped":
            suspicious_signals += 1
        if features.get("frequency_anomalies") == "high_frequency_grid_pattern":
            suspicious_signals += 1
        # GAN faces have unnaturally smooth skin (no pores/texture)
        if features.get("face_detected") and features.get("skin_smoothness", 0) > 0.85:
            suspicious_signals += 1

        if model_verdict and model_confidence is not None:
            if model_verdict == "manipulated" and model_confidence > 0.4:
                combined_confidence = model_confidence * 0.7 + min(suspicious_signals / 4, 1.0) * 0.3
                verdict = "manipulated"
            elif model_verdict == "real" and model_confidence > 0.4:
                # Strong rule-based signals can override a weak model "real" verdict
                rule_strength = min(suspicious_signals / 4, 1.0)
                combined_confidence = model_confidence * 0.7 + (1 - rule_strength) * 0.3
                # If multiple strong rule-based signals say fake, override model
                if suspicious_signals >= 3:
                    verdict = "manipulated"
                    combined_confidence = model_confidence * 0.4 + rule_strength * 0.6
                elif suspicious_signals >= 2 and model_confidence < 0.6:
                    verdict = "manipulated"
                    combined_confidence = rule_strength * 0.6 + (1 - model_confidence) * 0.4
                else:
                    verdict = "real"
            else:
                combined_confidence = min(suspicious_signals / 4, 1.0)
                verdict = "manipulated" if suspicious_signals >= 2 else "real"
        else:
            combined_confidence = min(suspicious_signals / 4, 1.0)
            verdict = "manipulated" if suspicious_signals >= 2 else "real"

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
        if features.get("metadata_integrity") == "exif_stripped" and severity in ("low", "medium"):
            severity = "medium"

        return verdict, combined_confidence, severity


# Singleton instance
image_detector = ImageDetector()
