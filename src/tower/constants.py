"""Variables that are needed in multiple files and don't change."""

from pathlib import Path


# Screen
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Platformer"

# Paths
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
ASSETS_DIR = ROOT_DIR / "assets"
LEVELS_DIR = ASSETS_DIR / "levels"
