import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "DeepFakeGuard"
    app_version: str = "1.0.0"
    debug: bool = False

    # Claude API
    anthropic_api_key: str = ""

    # ML Models
    model_audio: str = "garystafford/wav2vec2-deepfake-voice-detector"
    model_image: str = "buildborderless/CommunityForensics-DeepfakeDet-ViT"
    model_image_ensemble: str = "prithivMLmods/deepfake-detector-model-v1"
    models_dir: str = str(Path(__file__).parent.parent / "ml" / "models")

    # Limits
    max_audio_size_mb: int = 50
    max_image_size_mb: int = 20

    # Database
    database_url: str = "sqlite:///./deepfakeguard.db"

    # Logging
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
