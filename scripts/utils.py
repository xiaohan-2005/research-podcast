from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def data_dir() -> Path:
    return (Path.home() / ".research-podcast").resolve()


def load_config() -> dict[str, Any]:
    path = data_dir() / "config.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def ensure_output_dirs() -> None:
    root = data_dir()
    for name in ("episodes", "runs", "logs"):
        (root / name).mkdir(parents=True, exist_ok=True)
