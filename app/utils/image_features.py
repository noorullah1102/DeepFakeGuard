"""Image feature extraction utilities using OpenCV and NumPy."""

import io
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS

ALLOWED_IMAGE = {".jpg", ".jpeg", ".png", ".webp"}


def validate_image_file(filename: str) -> str:
    """Validate image file extension. Returns extension or raises ValueError."""
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_IMAGE:
        raise ValueError(
            f"File type '{ext}' is not supported. Accepted: {', '.join(sorted(ALLOWED_IMAGE))}"
        )
    return ext


def load_image(image_bytes: bytes) -> np.ndarray:
    """Load image bytes into a numpy array (BGR format for OpenCV)."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image file")
    return img


def extract_features(image: np.ndarray) -> dict:
    """Extract image features for deepfake analysis."""
    h, w = image.shape[:2]

    # --- Frequency domain analysis (FFT) ---
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fft = np.fft.fft2(gray)
    fft_shift = np.fft.fftshift(fft)
    magnitude = np.abs(fft_shift)

    h_half, w_half = h // 2, w // 2
    center_size = min(h, w) // 8
    low_freq = magnitude[
        h_half - center_size : h_half + center_size,
        w_half - center_size : w_half + center_size,
    ]
    total_energy = float(np.sum(magnitude))
    low_energy = float(np.sum(low_freq))
    high_freq_ratio = 1.0 - (low_energy / total_energy) if total_energy > 0 else 0.0

    log_magnitude = np.log1p(magnitude)
    freq_std = float(np.std(log_magnitude))
    has_gan_artifacts = freq_std < 2.0 and high_freq_ratio > 0.7

    if has_gan_artifacts:
        frequency_anomalies = "high_frequency_grid_pattern"
    elif high_freq_ratio > 0.8:
        frequency_anomalies = "unusual_high_freq_energy"
    else:
        frequency_anomalies = "normal_distribution"

    # --- Face detection ---
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    gray_small = cv2.resize(gray, (min(w, 800), min(h, 800)))
    faces = face_cascade.detectMultiScale(gray_small, scaleFactor=1.1, minNeighbors=5)
    face_detected = len(faces) > 0

    # --- Facial symmetry ---
    facial_symmetry = 0.0
    if face_detected:
        fx, fy, fw, fh = faces[0]
        face_roi = gray_small[fy : fy + fh, fx : fx + fw]
        face_roi = cv2.resize(face_roi, (100, 100))
        left_half = face_roi[:, :50]
        right_half = cv2.flip(face_roi[:, 50:], 1)
        diff = np.abs(left_half.astype(float) - right_half.astype(float))
        symmetry = 1.0 - (np.mean(diff) / 255.0)
        facial_symmetry = round(float(symmetry), 2)

    # --- Lighting consistency ---
    h2, w2 = h // 2, w // 2
    quadrants = [
        gray[:h2, :w2],
        gray[:h2, w2:],
        gray[h2:, :w2],
        gray[h2:, w2:],
    ]
    quad_means = [float(np.mean(q)) for q in quadrants]
    lighting_consistency = round(1.0 - (np.std(quad_means) / 128.0), 2)
    lighting_consistency = max(0.0, min(1.0, lighting_consistency))

    # --- Skin texture smoothness (GAN face detector) ---
    # StyleGAN faces lack natural skin texture (pores, fine lines).
    # Measure via local variance in the face region — too smooth = suspicious.
    skin_smoothness = 0.0
    if face_detected:
        fx, fy, fw, fh = faces[0]
        # Focus on cheek/forehead area (center of face)
        margin_x = int(fw * 0.2)
        margin_y = int(fh * 0.2)
        face_region = gray_small[
            fy + margin_y : fy + fh - margin_y,
            fx + margin_x : fx + fw - margin_x,
        ]
        if face_region.size > 0:
            # Local variance using Laplacian (measures texture detail)
            laplacian = cv2.Laplacian(face_region, cv2.CV_64F)
            local_var = float(np.var(laplacian))
            # Real skin has variance ~500-2000, GAN skin is often ~50-300
            # Normalize to 0-1 scale where 1.0 = suspiciously smooth
            skin_smoothness = round(max(0.0, min(1.0, 1.0 - (local_var - 50) / 1500)), 2)

    # --- Metadata integrity ---
    metadata_integrity = check_metadata_integrity(image)

    return {
        "gan_artifacts": has_gan_artifacts,
        "frequency_anomalies": frequency_anomalies,
        "facial_symmetry": facial_symmetry,
        "lighting_consistency": lighting_consistency,
        "metadata_integrity": metadata_integrity,
        "face_detected": face_detected,
        "skin_smoothness": skin_smoothness,
        "image_dimensions": f"{w}x{h}",
    }


def check_metadata_integrity(image_bytes_or_pil_source) -> str:
    """Check EXIF metadata status.

    AI-generated images typically have stripped or minimal EXIF data.
    Real camera photos usually have rich EXIF data (camera model, settings, etc).
    """
    try:
        if isinstance(image_bytes_or_pil_source, bytes):
            img = Image.open(io.BytesIO(image_bytes_or_pil_source))
        else:
            return "unknown"
    except Exception:
        return "unknown"

    exif_data = img._getexif()
    if exif_data is None:
        return "exif_stripped"

    camera_tags = {
        271: "Make",
        272: "Model",
        33434: "ExposureTime",
        33437: "FNumber",
        37500: "MakerNote",
        36867: "DateTimeOriginal",
    }
    found_camera_tags = sum(1 for tag_id in camera_tags if tag_id in exif_data)

    if found_camera_tags >= 3:
        return "clean"
    elif found_camera_tags >= 1:
        return "partial"
    else:
        return "exif_stripped"
