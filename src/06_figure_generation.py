from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import ZONE_ORDER


def run(tables_dir: Path, figures_dir: Path) -> None:
    arcs = pd.read_csv(tables_dir / "genre_arcs_with_film_bootstrap_ci.csv")
    counts = pd.read_csv(tables_dir / "primary_genre_film_counts.csv")
    top = counts.head(8)
    count_map = dict(zip(counts.genre, counts.n_films))

    plot = arcs[(arcs.genre_mode == "primary") & (arcs.method == "Full dialogue") & arcs.genre.isin(top.genre)]
    fig, ax = plt.subplots(figsize=(12, 7))
    x = np.arange(len(ZONE_ORDER))
    for genre, group in plot.groupby("genre"):
        group = group.set_index("story_zone").reindex(ZONE_ORDER)
        y = group.mean_sentiment.to_numpy(float)
        ax.plot(x, y, marker="o", label=f"{genre} (n={count_map[genre]})")
        ax.fill_between(x, group.ci_low.to_numpy(float), group.ci_high.to_numpy(float), alpha=.12)
    ax.axhline(0, color="black", linewidth=.8, linestyle="--")
    ax.set(xticks=x, xticklabels=ZONE_ORDER, xlabel="Story zone", ylabel="Mean film-level VADER sentiment",
           title="Primary-genre sentiment arcs with 95% film-bootstrap intervals")
    ax.legend(ncol=2, fontsize=9)
    fig.tight_layout()
    fig.savefig(figures_dir / "primary_genre_sentiment_arcs.png", dpi=200)
    fig.savefig(figures_dir / "primary_genre_sentiment_arcs.pdf")
    plt.close(fig)

    methods = arcs[(arcs.genre_mode == "primary") & arcs.genre.isin(top.genre)]
    method_avg = methods.groupby(["method", "story_zone"], as_index=False, observed=True).mean(numeric_only=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    for method, group in method_avg.groupby("method"):
        group["story_zone"] = pd.Categorical(group.story_zone, ZONE_ORDER, ordered=True)
        group = group.sort_values("story_zone")
        ax.plot(x, group.mean_sentiment, marker="o", label=method)
    ax.axhline(0, color="black", linewidth=.8, linestyle="--")
    ax.set(xticks=x, xticklabels=ZONE_ORDER, xlabel="Story zone", ylabel="Mean film-level VADER sentiment",
           title="Full dialogue, TF-IDF filtering, and frequency baseline")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figures_dir / "dialogue_method_comparison.png", dpi=200)
    fig.savefig(figures_dir / "dialogue_method_comparison.pdf")
    plt.close(fig)
