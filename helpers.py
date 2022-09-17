import json
from pathlib import Path


def get_config() -> dict[str, str]:

    root_dir = Path(".")
    config_fp = root_dir / "config.json"
    with open(config_fp, "r") as f:
        return json.load(f)
