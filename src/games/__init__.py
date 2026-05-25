"""Shared game registry instance."""

from pathlib import Path
from src.games.registry import GameRegistry

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_DIR = PROJECT_ROOT / "data" / "games"
USER_DIR = PROJECT_ROOT / "user_data" / "games"

registry = GameRegistry()

try:
    registry.load_definitions(app_directory=APP_DIR, user_directory=USER_DIR)
except Exception as e:
    raise RuntimeError(f"Failed to load game definitions: {e}") from e
