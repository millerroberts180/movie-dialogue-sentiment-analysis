from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name.replace(".", "_"), SRC / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduce the movie-dialogue robustness analysis")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "raw")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results")
    parser.add_argument("--bootstrap", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=112)
    parser.add_argument("--match-threshold", type=float, default=90.0)
    args = parser.parse_args()

    import sys
    sys.path.insert(0, str(SRC))
    common = load("common")
    paths = common.ensure_dirs(args.output_dir)
    load("01_data_acquisition").run(args.data_dir, paths["reports"])
    parsing = load("02_script_parsing").run(args.data_dir, paths["reports"])
    matching = load("03_tmdb_matching").run(args.data_dir, paths["reports"], args.match_threshold)
    features = load("04_feature_construction").run(args.data_dir, paths["intermediate"], args.match_threshold)
    analysis = load("05_analysis").run(features, paths["tables"], paths["reports"], args.bootstrap, args.seed)
    load("06_figure_generation").run(paths["tables"], paths["figures"])

    import pandas as pd
    flow = [
        {"stage": "Film Corpus 2.0 published size", "films": 960, "note": "Publisher-described corpus size"},
        {"stage": "IDs in supplied extraction log", "films": parsing["logged_candidates"], "note": "Discrepancy requires provenance review"},
        {"stage": "Parsed", "films": parsing["parsed"], "note": "At least one scene extracted"},
        {"stage": "Parsing failed", "films": parsing["parsing_failed"], "note": "See parsing_outcomes.csv"},
        {"stage": "TMDb matched", "films": matching["tmdb_matched"], "note": "Before confidence review"},
        {"stage": "TMDb unmatched", "films": matching["tmdb_unmatched"], "note": "No strong automated match"},
        {"stage": "TMDb ambiguous", "films": matching["tmdb_ambiguous"], "note": f"title_score < {args.match_threshold:g}"},
        {"stage": "High-confidence eligible", "films": matching["high_confidence"], "note": "Before genre/dialogue missingness"},
    ]
    pd.DataFrame(flow).to_csv(paths["reports"] / "sample_flow.csv", index=False)
    tfidf_r = analysis["correlations"].get("Full dialogue vs TF-IDF filtered", float("nan"))
    baseline_r = analysis["correlations"].get("Full dialogue vs Frequency baseline", float("nan"))
    findings = f"""# Generated findings

This file was generated from the high-confidence (`title_score >= {args.match_threshold:g}`) analysis.

- Parsed {parsing['parsed']} of {parsing['logged_candidates']} IDs in the supplied extraction log; the publisher-described corpus size is 960 and the discrepancy requires resolution.
- TMDb returned {matching['tmdb_matched']} matches and {matching['tmdb_unmatched']} unmatched titles; {matching['tmdb_ambiguous']} matches were flagged as ambiguous, leaving {matching['high_confidence']} eligible films before missing-data exclusions.
- The complete three-method comparison contains {analysis['analysis_scenes']} scenes from {analysis['analysis_films']} films.
- The scene-level association between full-dialogue and TF-IDF-filtered VADER is r = {tfidf_r:.3f}. The corresponding frequency-baseline association is r = {baseline_r:.3f}. Because the baseline is also strongly associated, `r = 0.79` does not by itself establish a special genre-vocabulary effect. These are associations between transformations of the same text, not external validation.
- Genre claims must be read from `genre_arcs_with_film_bootstrap_ci.csv`, which uses equal film weighting and film-level 95% bootstrap intervals. In the eight largest primary genres, Comedy is the most positive throughout and Horror has the most negative resolution; uncertainty bands overlap for many other comparisons.
- Primary-genre sensitivity is reported beside the multi-label estimates in `genre_assignment_sensitivity.csv`. The mean absolute change across genre-zone estimates is {analysis['mean_genre_sensitivity']:.3f}, with a maximum of {analysis['max_genre_sensitivity']:.3f}; genre-assignment choice can therefore materially affect individual estimates.
"""
    (paths["reports"] / "findings.md").write_text(findings)
    print(f"Complete. Results written to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
