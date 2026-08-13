from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

ZONE_ORDER = ["Opening", "Inciting conflict", "Escalation", "Climax zone", "Resolution"]


def ensure_dirs(output_dir: Path) -> dict[str, Path]:
    paths = {
        "reports": output_dir / "reports",
        "tables": output_dir / "tables",
        "figures": output_dir / "figures",
        "intermediate": output_dir / "intermediate",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def assign_story_zone(position: float) -> str:
    if position <= 0.15:
        return "Opening"
    if position <= 0.30:
        return "Inciting conflict"
    if position <= 0.65:
        return "Escalation"
    if position <= 0.90:
        return "Climax zone"
    return "Resolution"


def split_genres(value: object) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return []
    cleaned = value.replace("[", "").replace("]", "").replace("'", "").replace('"', "")
    return [item.strip() for item in re.split(r",|\|", cleaned) if item.strip()]


def bootstrap_mean(values: pd.Series, rng: np.random.Generator, n_boot: int) -> tuple[float, float]:
    arr = values.dropna().to_numpy(dtype=float)
    if len(arr) < 2:
        return np.nan, np.nan
    draws = rng.choice(arr, size=(n_boot, len(arr)), replace=True).mean(axis=1)
    return tuple(np.quantile(draws, [0.025, 0.975]))
