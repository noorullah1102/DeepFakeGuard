"""Audio feature extraction utilities using Librosa."""

import io
import tempfile
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf


ALLOWED_AUDIO = {".wav", ".mp3", ".flac"}


def validate_audio_file(filename: str) -> str:
    """Validate audio file extension. Returns extension or raises ValueError."""
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_AUDIO:
        raise ValueError(
            f"File type '{ext}' is not supported. Accepted: {', '.join(sorted(ALLOWED_AUDIO))}"
        )
    return ext


def load_audio(audio_bytes: bytes, sr: int = 16000) -> tuple[np.ndarray, int]:
    """Load audio bytes into a numpy waveform array."""
    audio = sf.read(io.BytesIO(audio_bytes))
    # soundfile returns (data, samplerate)
    waveform, sample_rate = audio

    # Convert to mono if stereo
    if len(waveform.shape) > 1:
        waveform = waveform.mean(axis=1)

    # Resample if needed
    if sample_rate != sr:
        waveform = librosa.resample(waveform, orig_sr=sample_rate, target_sr=sr)

    return waveform.astype(np.float32), sr


def extract_features(waveform: np.ndarray, sr: int = 16000) -> dict:
    """Extract audio features for deepfake analysis.

    Returns a dict of raw features used for both rule-based checks
    and model input preparation.
    """
    duration = len(waveform) / sr

    # MFCCs (mel-frequency cepstral coefficients)
    mfccs = librosa.feature.mfcc(y=waveform, sr=sr, n_mfcc=13)
    mfcc_mean = float(np.mean(mfccs))
    mfcc_std = float(np.std(mfccs))

    # Spectral centroid (brightness of sound)
    spectral_centroid = librosa.feature.spectral_centroid(y=waveform, sr=sr)[0]
    centroid_mean = float(np.mean(spectral_centroid))

    # Spectral bandwidth
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=waveform, sr=sr)[0]
    bandwidth_mean = float(np.mean(spectral_bandwidth))

    # Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(waveform)[0]
    zcr_mean = float(np.mean(zcr))

    # Pitch estimation using pyin
    try:
        f0, voiced_flag, _ = librosa.pyin(
            waveform, fmin=librosa.note_to_hz("C2"), fmax=librosa.note_to_hz("C7"), sr=sr
        )
        valid_f0 = f0[~np.isnan(f0)] if f0 is not None else np.array([])
    except Exception:
        valid_f0 = np.array([])
    pitch_mean = float(np.mean(valid_f0)) if len(valid_f0) > 0 else 0.0
    pitch_std = float(np.std(valid_f0)) if len(valid_f0) > 0 else 0.0

    # RMS energy (for breathing / silence detection)
    rms = librosa.feature.rms(y=waveform)[0]
    rms_mean = float(np.mean(rms))

    # Detect silence segments (potential breathing gaps)
    silence_threshold = float(np.percentile(rms, 10))
    silence_frames = np.sum(rms < silence_threshold)
    total_frames = len(rms)
    silence_ratio = float(silence_frames / total_frames) if total_frames > 0 else 0.0

    # Background noise uniformity (std of RMS — low std = uniform noise)
    rms_std = float(np.std(rms))
    noise_uniformity = float(rms_std / rms_mean) if rms_mean > 0 else 0.0

    # Mel spectrogram (for model input)
    mel_spec = librosa.feature.melspectrogram(y=waveform, sr=sr, n_mels=80)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

    return {
        "duration_seconds": round(duration, 2),
        "mfcc_mean": mfcc_mean,
        "mfcc_std": mfcc_std,
        "spectral_centroid_mean": centroid_mean,
        "spectral_bandwidth_mean": bandwidth_mean,
        "zero_crossing_rate": zcr_mean,
        "pitch_mean": pitch_mean,
        "pitch_std": pitch_std,
        "rms_mean": rms_mean,
        "silence_ratio": silence_ratio,
        "noise_uniformity": noise_uniformity,
        "mel_spectrogram": mel_spec_db,
        "sample_rate": sr,
    }


def analyze_artifacts(features: dict) -> dict:
    """Run rule-based checks on extracted features to detect synthetic audio artifacts."""
    pitch_std = features["pitch_std"]
    pitch_mean = features["pitch_mean"]
    silence_ratio = features["silence_ratio"]
    noise_uniformity = features["noise_uniformity"]
    zcr = features["zero_crossing_rate"]

    # Pitch consistency: real speech has high pitch variation
    # Synthetic speech tends to have unnaturally stable pitch
    pitch_consistency = max(0.0, min(1.0, pitch_std / max(pitch_mean * 0.15, 1.0)))

    # Breathing patterns: natural speech has regular silence gaps
    # Synthetic speech often lacks natural breathing pauses
    if silence_ratio < 0.02:
        breathing = "absent"
    elif silence_ratio < 0.08:
        breathing = "irregular"
    else:
        breathing = "natural"

    # Background noise: synthetic audio often has suspiciously uniform noise
    if noise_uniformity < 0.3:
        background = "unnaturally_uniform"
    elif noise_uniformity < 0.7:
        background = "varying"
    else:
        background = "natural_variation"

    # Spectral artifacts: synthetic audio often has smoother spectral envelope
    spectral_artifacts = features["mfcc_std"] < 2.0 or zcr < 0.03

    # Codec artifacts heuristic
    if spectral_artifacts and pitch_consistency < 0.5:
        codec = "consistent_with_tts"
    else:
        codec = "natural_recording"

    return {
        "spectral_artifacts": spectral_artifacts,
        "pitch_consistency": round(pitch_consistency, 2),
        "breathing_patterns": breathing,
        "background_noise": background,
        "codec_artifacts": codec,
        "duration_seconds": features["duration_seconds"],
    }
