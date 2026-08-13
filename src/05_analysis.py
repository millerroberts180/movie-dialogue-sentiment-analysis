from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from common import ZONE_ORDER, bootstrap_mean

METHODS = {
    "Full dialogue": "sentiment_score",
    "TF-IDF filtered": "tfidf_filtered_sentiment",
    "Frequency baseline": "frequency_baseline_sentiment",
}


def _film_zone(df: pd.DataFrame, genre_mode: str) -> pd.DataFrame:
    base = df.copy()
    if genre_mode == "primary":
        base["analysis_genre"] = base["primary_genre"]
    else:
        base = base.explode("genre_list")
        base["analysis_genre"] = base["genre_list"]
    return (
        base.dropna(subset=["analysis_genre"])
        .groupby(["movie_id", "analysis_genre", "story_zone"], observed=True, as_index=False)
        .agg(**{label: (column, "mean") for label, column in METHODS.items()})
    )


def _summarize(film_zone: pd.DataFrame, mode: str, rng: np.random.Generator, n_boot: int) -> pd.DataFrame:
    rows = []
    for (genre, zone), group in film_zone.groupby(["analysis_genre", "story_zone"], observed=True):
        for method in METHODS:
            low, high = bootstrap_mean(group[method], rng, n_boot)
            rows.append({
                "genre_mode": mode, "genre": genre, "story_zone": zone, "method": method,
                "mean_sentiment": group[method].mean(), "ci_low": low, "ci_high": high,
                "n_films": group.loc[group[method].notna(), "movie_id"].nunique(),
            })
    return pd.DataFrame(rows)


def run(feature_path: Path, tables_dir: Path, reports_dir: Path, n_boot: int, seed: int) -> dict[str, float]:
    df = pd.read_pickle(feature_path)
    rng = np.random.default_rng(seed)
    all_summaries = []
    film_tables = {}
    for mode in ["primary", "multi_label"]:
        film_tables[mode] = _film_zone(df, mode)
        all_summaries.append(_summarize(film_tables[mode], mode, rng, n_boot))
    arcs = pd.concat(all_summaries, ignore_index=True)
    arcs["story_zone"] = pd.Categorical(arcs["story_zone"], ZONE_ORDER, ordered=True)
    arcs.sort_values(["genre_mode", "genre", "method", "story_zone"]).to_csv(
        tables_dir / "genre_arcs_with_film_bootstrap_ci.csv", index=False
    )

    primary_full = arcs[(arcs.genre_mode == "primary") & (arcs.method == "Full dialogue")]
    multi_full = arcs[(arcs.genre_mode == "multi_label") & (arcs.method == "Full dialogue")]
    sensitivity = primary_full.merge(
        multi_full, on=["genre", "story_zone", "method"], suffixes=("_primary", "_multi")
    )
    sensitivity["multi_minus_primary"] = sensitivity.mean_sentiment_multi - sensitivity.mean_sentiment_primary
    sensitivity.to_csv(tables_dir / "genre_assignment_sensitivity.csv", index=False)

    comparisons = []
    valid = df.dropna(subset=list(METHODS.values()))
    for label, column in list(METHODS.items())[1:]:
        comparisons.append({
            "comparison": f"Full dialogue vs {label}",
            "scene_level_pearson_r": valid["sentiment_score"].corr(valid[column]),
            "mean_absolute_difference": (valid["sentiment_score"] - valid[column]).abs().mean(),
            "n_scenes": len(valid), "n_films": valid.movie_id.nunique(),
        })
    comparison_df = pd.DataFrame(comparisons)
    comparison_df.to_csv(tables_dir / "dialogue_method_comparison.csv", index=False)

    film_counts = primary_full.groupby("genre", as_index=False).n_films.max().sort_values("n_films", ascending=False)
    film_counts.to_csv(tables_dir / "primary_genre_film_counts.csv", index=False)
    return {
        "correlations": {row.comparison: row.scene_level_pearson_r for row in comparison_df.itertuples()},
        "analysis_films": int(valid["movie_id"].nunique()),
        "analysis_scenes": int(len(valid)),
        "max_genre_sensitivity": float(sensitivity["multi_minus_primary"].abs().max()),
        "mean_genre_sensitivity": float(sensitivity["multi_minus_primary"].abs().mean()),
    }
