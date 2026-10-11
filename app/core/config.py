from pathlib import Path
import os

APP_NAME = os.getenv("APP_NAME", "GRU Sentence Generator API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
# Docker runs from /app. Local development runs from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
_default_artifact_dir = PROJECT_ROOT / "artifacts"
MODEL_DIR = Path(os.getenv("MODEL_DIR", str(_default_artifact_dir))).expanduser().resolve()
MODEL_FILE = os.getenv("MODEL_FILE", "sentence_generator_gru.keras")
TOKENIZER_FILE = os.getenv("TOKENIZER_FILE", "tokenizer.pkl")
MAX_LEN_FILE = os.getenv("MAX_LEN_FILE", "max_len.pkl")
