from pathlib import Path

import appdirs

ROOT_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT_DIR / "assets"

CONFIG_FILE = Path(appdirs.user_config_dir("clockpi")) / "config.yml"
