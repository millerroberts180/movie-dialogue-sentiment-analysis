from __future__ import annotations

from pathlib import Path

import pandas as pd


def run(data_dir: Path, reports_dir: Path, threshold: float = 90.0) -> dict[str, int]:
    metadata = pd.read_csv(data_dir / "tmdb_api_movie_metadata.csv")
    unmatched = pd.read_csv(data_dir / "tmdb_api_unmatched_movies.csv")
    if metadata["movie_id"].duplicated().any():
        raise ValueError("TMDb metadata contains duplicate movie_id values")
    ambiguous = metadata.loc[metadata["title_score"] < threshold].copy()
    ambiguous.insert(0, "review_reason", f"title_score < {threshold:g}")
    ambiguous.to_csv(reports_dir / "ambiguous_tmdb_matches.csv", index=False)
    unmatched.to_csv(reports_dir / "unmatched_tmdb_titles.csv", index=False)
    return {
        "tmdb_matched": int(metadata["movie_id"].nunique()),
        "tmdb_unmatched": int(unmatched["movie_id"].nunique()),
        "tmdb_ambiguous": int(ambiguous["movie_id"].nunique()),
        "high_confidence": int(metadata.loc[metadata["title_score"] >= threshold, "movie_id"].nunique()),
    }
