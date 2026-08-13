from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED = [
    "scene_extraction_log.csv",
    "tmdb_api_movie_metadata.csv",
    "tmdb_api_unmatched_movies.csv",
    "scene_level_tfidf_filtered_sentiment.csv",
]


def run(data_dir: Path, reports_dir: Path) -> None:
    rows = []
    for name in REQUIRED:
        path = data_dir / name
        if not path.exists():
            raise FileNotFoundError(f"Required input is missing: {path}")
        rows.append({"artifact": name, "bytes": path.stat().st_size, "status": "present"})
    pd.DataFrame(rows).to_csv(reports_dir / "input_inventory.csv", index=False)
