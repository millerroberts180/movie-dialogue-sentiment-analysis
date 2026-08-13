from __future__ import annotations

from pathlib import Path

import pandas as pd


def run(data_dir: Path, reports_dir: Path) -> dict[str, int]:
    log = pd.read_csv(data_dir / "scene_extraction_log.csv")
    if log["movie_id"].duplicated().any():
        raise ValueError("Parsing log contains duplicate movie_id values")
    counts = log.groupby(["status", "reason"], dropna=False).size().rename("films").reset_index()
    counts.to_csv(reports_dir / "parsing_outcomes.csv", index=False)
    return {
        "logged_candidates": int(log["movie_id"].nunique()),
        "parsed": int(log.loc[log["status"].eq("processed"), "movie_id"].nunique()),
        "parsing_failed": int(log.loc[~log["status"].eq("processed"), "movie_id"].nunique()),
    }
