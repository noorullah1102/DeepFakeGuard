"""Baseline benchmark for image deepfake detector against CIFAKE dataset.

Downloads a sample from CIFAKE (real CIFAR-10 vs Stable Diffusion fakes),
runs the full detection pipeline, and reports standard ML metrics.

Usage:
    source venv/bin/activate
    python scripts/benchmark_image.py [--sample N]
"""

import argparse
import io
import json
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

# Add project root to path so we can import app modules
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.services.image_detector import ImageDetector


def download_dataset(sample_per_class: int = 100) -> list[tuple[bytes, int, str]]:
    """Download deepfake test dataset and return (image_bytes, label, source) tuples.

    Dataset: itsLeen/deepfake_vs_real_image_detection (512x512+ images)
    Labels: 0 = real, 1 = fake.
    """
    from datasets import load_dataset

    print("Downloading deepfake dataset (itsLeen/deepfake_vs_real_image_detection)...")
    dataset = load_dataset(
        "itsLeen/deepfake_vs_real_image_detection", split="test", streaming=True
    ).shuffle(seed=42)

    real_samples = []
    fake_samples = []

    for row in dataset:
        if row["label"] == 0 and len(real_samples) < sample_per_class:
            real_samples.append(row)
        elif row["label"] == 1 and len(fake_samples) < sample_per_class:
            fake_samples.append(row)

        if len(real_samples) >= sample_per_class and len(fake_samples) >= sample_per_class:
            break

    print(f"  Real images: {len(real_samples)}, Fake images: {len(fake_samples)}")

    samples = []
    for i, row in enumerate(real_samples):
        img = row["image"].convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        samples.append((buf.getvalue(), 0, f"real_{i:04d}"))

    for i, row in enumerate(fake_samples):
        img = row["image"].convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        samples.append((buf.getvalue(), 1, f"fake_{i:04d}"))

    return samples


def run_individual_model(detector: ImageDetector, image_bytes: bytes) -> dict | None:
    """Run each sub-model individually to get per-model predictions."""
    import torch

    results = {}
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # CommunityForensics ViT
    if detector._model_loaded:
        try:
            import torchvision.transforms as T

            transform = T.Compose([
                T.Resize((384, 384), interpolation=T.InterpolationMode.BICUBIC),
                T.ToTensor(),
                T.Normalize(mean=[0.4815, 0.4578, 0.4082], std=[0.2686, 0.2613, 0.2758]),
            ])
            pixel_values = transform(image).unsqueeze(0)
            with torch.no_grad():
                logits = detector.model(pixel_values=pixel_values).logits
            probs = torch.softmax(logits, dim=-1)
            results["communityforensics"] = {
                "fake_prob": probs[0][1].item(),
                "verdict": "manipulated" if probs[0][1].item() > 0.5 else "real",
            }
        except Exception:
            results["communityforensics"] = None

    # prithivMLmods SigLIP
    if detector._ensemble_loaded:
        try:
            inputs = detector.processor_ensemble(images=image, return_tensors="pt")
            with torch.no_grad():
                logits = detector.model_ensemble(**inputs).logits
            probs = torch.softmax(logits, dim=-1)
            results["prithivmlmods"] = {
                "fake_prob": probs[0][0].item(),
                "verdict": "manipulated" if probs[0][0].item() > 0.5 else "real",
            }
        except Exception:
            results["prithivmlmods"] = None

    return results


def run_benchmark(sample_per_class: int = 100):
    """Run the full benchmark and print results."""
    print("=" * 60)
    print("DeepFakeGuard — Image Detector Baseline Benchmark")
    print("=" * 60)
    print()

    # Download dataset
    samples = download_dataset(sample_per_class)
    print()

    # Load detector
    print("Loading image detection models...")
    detector = ImageDetector()
    detector.load_model()
    if not detector.is_loaded:
        print("ERROR: No models loaded. Cannot run benchmark.")
        sys.exit(1)
    print(f"  Primary (CommunityForensics): {'loaded' if detector._model_loaded else 'FAILED'}")
    print(f"  Ensemble (prithivMLmods):     {'loaded' if detector._ensemble_loaded else 'FAILED'}")
    print()

    # Run detection
    print(f"Running detection on {len(samples)} images...")
    y_true = []
    y_pred = []
    y_pred_cf = []  # CommunityForensics predictions
    y_pred_pm = []  # prithivMLmods predictions
    confidences = []
    details = []

    start = time.time()
    for i, (img_bytes, label, source) in enumerate(samples):
        result = detector.detect(img_bytes, filename=f"{source}.jpg")
        pred_label = 1 if result["verdict"] == "manipulated" else 0

        y_true.append(label)
        y_pred.append(pred_label)
        confidences.append(result["confidence"])

        # Per-model breakdown
        per_model = run_individual_model(detector, img_bytes)
        if per_model.get("communityforensics"):
            y_pred_cf.append(1 if per_model["communityforensics"]["verdict"] == "manipulated" else 0)
        if per_model.get("prithivmlmods"):
            y_pred_pm.append(1 if per_model["prithivmlmods"]["verdict"] == "manipulated" else 0)

        details.append({
            "source": source,
            "label": "real" if label == 0 else "fake",
            "predicted": result["verdict"],
            "confidence": result["confidence"],
            "severity": result["severity"],
            "correct": pred_label == label,
            "communityforensics": per_model.get("communityforensics"),
            "prithivmlmods": per_model.get("prithivmlmods"),
        })

        if (i + 1) % 20 == 0:
            print(f"  Processed {i + 1}/{len(samples)}")

    elapsed = time.time() - start
    print(f"  Done in {elapsed:.1f}s ({elapsed / len(samples):.2f}s/image)")
    print()

    # Compute metrics
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # --- Full Pipeline ---
    print("=" * 60)
    print("FULL PIPELINE (ML Ensemble + Rule-Based)")
    print("=" * 60)
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, pos_label=1, zero_division=0)
    rec = recall_score(y_true, y_pred, pos_label=1, zero_division=0)
    f1 = f1_score(y_true, y_pred, pos_label=1, zero_division=0)
    cm = confusion_matrix(y_true, y_pred)

    print(f"  Accuracy:  {acc:.3f}")
    print(f"  Precision: {prec:.3f}  (of predicted fake, how many actually fake)")
    print(f"  Recall:    {rec:.3f}  (of actual fake, how many caught)")
    print(f"  F1 Score:  {f1:.3f}")
    print()
    print(f"  Confusion Matrix:")
    print(f"                Predicted")
    print(f"                Real  Fake")
    print(f"  Actual Real   {cm[0][0]:>4}  {cm[0][1]:>4}")
    print(f"  Actual Fake   {cm[1][0]:>4}  {cm[1][1]:>4}")
    print()

    real_mask = y_true == 0
    fake_mask = y_true == 1
    print(f"  Real images correct:  {np.sum((y_pred == 0) & real_mask)}/{np.sum(real_mask)}")
    print(f"  Fake images correct:  {np.sum((y_pred == 1) & fake_mask)}/{np.sum(fake_mask)}")
    print(f"  Avg confidence:       {np.mean(confidences):.3f}")
    print()

    # --- Per-Model Breakdown ---
    if y_pred_cf:
        print("=" * 60)
        print("CommunityForensics ViT (Primary)")
        print("=" * 60)
        y_pred_cf = np.array(y_pred_cf)
        acc_cf = accuracy_score(y_true, y_pred_cf)
        f1_cf = f1_score(y_true, y_pred_cf, pos_label=1, zero_division=0)
        print(f"  Accuracy: {acc_cf:.3f}   F1: {f1_cf:.3f}")
        cm_cf = confusion_matrix(y_true, y_pred_cf)
        print(f"  Confusion Matrix:")
        print(f"                Predicted")
        print(f"                Real  Fake")
        print(f"  Actual Real   {cm_cf[0][0]:>4}  {cm_cf[0][1]:>4}")
        print(f"  Actual Fake   {cm_cf[1][0]:>4}  {cm_cf[1][1]:>4}")
        print()

    if y_pred_pm:
        print("=" * 60)
        print("prithivMLmods SigLIP (Ensemble)")
        print("=" * 60)
        y_pred_pm = np.array(y_pred_pm)
        acc_pm = accuracy_score(y_true, y_pred_pm)
        f1_pm = f1_score(y_true, y_pred_pm, pos_label=1, zero_division=0)
        print(f"  Accuracy: {acc_pm:.3f}   F1: {f1_pm:.3f}")
        cm_pm = confusion_matrix(y_true, y_pred_pm)
        print(f"  Confusion Matrix:")
        print(f"                Predicted")
        print(f"                Real  Fake")
        print(f"  Actual Real   {cm_pm[0][0]:>4}  {cm_pm[0][1]:>4}")
        print(f"  Actual Fake   {cm_pm[1][0]:>4}  {cm_pm[1][1]:>4}")
        print()

    # --- Summary comparison ---
    print("=" * 60)
    print("COMPARISON")
    print("=" * 60)
    print(f"  {'Model':<35} {'Accuracy':>10} {'F1':>8}")
    print(f"  {'-'*35} {'-'*10} {'-'*8}")
    print(f"  {'Full Pipeline (Ensemble + Rules)':<35} {acc:>10.3f} {f1:>8.3f}")
    if y_pred_cf is not None and len(y_pred_cf):
        print(f"  {'CommunityForensics ViT':<35} {acc_cf:>10.3f} {f1_cf:>8.3f}")
    if y_pred_pm is not None and len(y_pred_pm):
        print(f"  {'prithivMLmods SigLIP':<35} {acc_pm:>10.3f} {f1_pm:>8.3f}")
    print()

    # Save results
    results = {
        "dataset": "itsLeen/deepfake_vs_real_image_detection",
        "samples": {"real": int(np.sum(real_mask)), "fake": int(np.sum(fake_mask))},
        "full_pipeline": {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1": round(float(f1), 4),
            "confusion_matrix": cm.tolist(),
            "avg_confidence": round(float(np.mean(confidences)), 4),
        },
        "communityforensics_vit": {
            "accuracy": round(float(acc_cf), 4),
            "f1": round(float(f1_cf), 4),
        } if y_pred_cf is not None and len(y_pred_cf) else None,
        "prithivmlmods_siglip": {
            "accuracy": round(float(acc_pm), 4),
            "f1": round(float(f1_pm), 4),
        } if y_pred_pm is not None and len(y_pred_pm) else None,
        "per_image_details": details,
    }

    output_path = ROOT / "scripts" / "benchmark_results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark image deepfake detector")
    parser.add_argument(
        "--sample",
        type=int,
        default=100,
        help="Number of images per class (default: 100)",
    )
    args = parser.parse_args()
    run_benchmark(sample_per_class=args.sample)
