"""Baseline benchmark for audio deepfake detector against labeled dataset.

Downloads a sample from UniDataPro/real-vs-fake-human-voice-deepfake-audio,
runs the full detection pipeline, and reports standard ML metrics.

Usage:
    source venv/bin/activate
    python scripts/benchmark_audio.py [--sample N]
"""

import argparse
import io
import json
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.services.audio_detector import AudioDetector


def download_dataset(sample_per_class: int = 50) -> list[tuple[bytes, int, str]]:
    """Download audio deepfake dataset and return (audio_bytes, label, source) tuples.

    Dataset: UniDataPro/real-vs-fake-human-voice-deepfake-audio
    Labels: 0 = real, 1 = fake.
    """
    from datasets import load_dataset

    print("Downloading audio dataset (UniDataPro/real-vs-fake-human-voice-deepfake-audio)...")
    dataset = load_dataset(
        "UniDataPro/real-vs-fake-human-voice-deepfake-audio",
        split="train",
        streaming=True,
    ).shuffle(seed=42)

    real_samples = []
    fake_samples = []

    for row in dataset:
        arr = row["audio"]["array"]
        sr = row["audio"]["sampling_rate"]
        label = row["label"]

        # Convert numpy array to WAV bytes
        buf = io.BytesIO()
        sf.write(buf, arr, sr, format='WAV')
        wav_bytes = buf.getvalue()

        if label == 0 and len(real_samples) < sample_per_class:
            real_samples.append((wav_bytes, 0, f"real_{len(real_samples):04d}"))
        elif label == 1 and len(fake_samples) < sample_per_class:
            fake_samples.append((wav_bytes, 1, f"fake_{len(fake_samples):04d}"))

        if len(real_samples) >= sample_per_class and len(fake_samples) >= sample_per_class:
            break

    print(f"  Real audio: {len(real_samples)}, Fake audio: {len(fake_samples)}")
    return real_samples + fake_samples


def run_benchmark(sample_per_class: int = 50):
    """Run the full benchmark and print results."""
    print("=" * 60)
    print("DeepFakeGuard — Audio Detector Baseline Benchmark")
    print("=" * 60)
    print()

    samples = download_dataset(sample_per_class)
    print()

    print("Loading audio detection model...")
    detector = AudioDetector()
    detector.load_model()
    if not detector.is_loaded:
        print("ERROR: Audio model not loaded. Cannot run benchmark.")
        sys.exit(1)
    print(f"  Wav2Vec2 model: loaded")
    print()

    print(f"Running detection on {len(samples)} audio clips...")
    y_true = []
    y_pred = []
    confidences = []
    details = []

    start = time.time()
    for i, (audio_bytes, label, source) in enumerate(samples):
        result = detector.detect(audio_bytes, filename=f"{source}.wav")
        pred_label = 1 if result["verdict"] == "synthetic" else 0

        y_true.append(label)
        y_pred.append(pred_label)
        confidences.append(result["confidence"])

        details.append({
            "source": source,
            "label": "real" if label == 0 else "fake",
            "predicted": result["verdict"],
            "confidence": result["confidence"],
            "severity": result["severity"],
            "correct": pred_label == label,
            "duration": result["analysis"].get("duration_seconds", 0),
        })

        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(samples)}")

    elapsed = time.time() - start
    print(f"  Done in {elapsed:.1f}s ({elapsed / len(samples):.2f}s/clip)")
    print()

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # --- Metrics ---
    print("=" * 60)
    print("FULL PIPELINE (Wav2Vec2 + Rule-Based)")
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
    print(f"                  Predicted")
    print(f"                  Real  Fake")
    print(f"  Actual Real     {cm[0][0]:>4}  {cm[0][1]:>4}")
    print(f"  Actual Fake     {cm[1][0]:>4}  {cm[1][1]:>4}")
    print()

    real_mask = y_true == 0
    fake_mask = y_true == 1
    print(f"  Real audio correct:  {np.sum((y_pred == 0) & real_mask)}/{np.sum(real_mask)}")
    print(f"  Fake audio correct:  {np.sum((y_pred == 1) & fake_mask)}/{np.sum(fake_mask)}")
    print(f"  Avg confidence:      {np.mean(confidences):.3f}")
    print()

    # Save results
    results = {
        "dataset": "UniDataPro/real-vs-fake-human-voice-deepfake-audio",
        "samples": {"real": int(np.sum(real_mask)), "fake": int(np.sum(fake_mask))},
        "model": "garystafford/wav2vec2-deepfake-voice-detector",
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1": round(float(f1), 4),
        "confusion_matrix": cm.tolist(),
        "avg_confidence": round(float(np.mean(confidences)), 4),
        "per_clip_details": details,
    }

    output_path = ROOT / "scripts" / "benchmark_audio_results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark audio deepfake detector")
    parser.add_argument(
        "--sample",
        type=int,
        default=50,
        help="Number of audio clips per class (default: 50)",
    )
    args = parser.parse_args()
    run_benchmark(sample_per_class=args.sample)
