from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from common import ZONE_ORDER, assign_story_zone, split_genres

TOKEN_RE = re.compile(r"[A-Za-z']+")


def _tokens(text: object) -> list[str]:
    return [t for t in TOKEN_RE.findall(str(text).lower()) if t not in ENGLISH_STOP_WORDS]


def run(data_dir: Path, intermediate_dir: Path, threshold: float = 90.0) -> Path:
    source = pd.read_csv(data_dir / "scene_level_tfidf_filtered_sentiment.csv")
    metadata = pd.read_csv(data_dir / "tmdb_api_movie_metadata.csv", usecols=["movie_id", "title_score"])
    eligible = set(metadata.loc[metadata["title_score"] >= threshold, "movie_id"])
    df = source.loc[source["movie_id"].isin(eligible)].copy()
    df["dialogue_text"] = df["dialogue_text"].fillna("")
    df["tfidf_filtered_dialogue"] = df["tfidf_filtered_dialogue"].fillna("")
    df["story_zone"] = df["relative_position"].apply(assign_story_zone)
    df["story_zone"] = pd.Categorical(df["story_zone"], ZONE_ORDER, ordered=True)
    df["genre_list"] = df["genre"].apply(split_genres)
    df["primary_genre"] = df["genre_list"].str[0]

    # The baseline uses common content words and exactly matches each scene's
    # supplied TF-IDF retained-token count, preventing text length from being
    # the explanation for method differences.
    token_lists = df["dialogue_text"].map(_tokens)
    frequencies = Counter(token for tokens in token_lists for token in tokens)
    ranks = {token: rank for rank, (token, _) in enumerate(frequencies.most_common())}

    def baseline_text(row_tokens: list[str], target_text: str) -> str:
        k = len(TOKEN_RE.findall(target_text))
        if k == 0:
            return ""
        ordered = sorted(enumerate(row_tokens), key=lambda pair: (ranks.get(pair[1], 10**12), pair[0]))
        chosen_positions = sorted(pos for pos, _ in ordered[:k])
        return " ".join(row_tokens[pos] for pos in chosen_positions)

    df["frequency_baseline_dialogue"] = [
        baseline_text(tokens, filtered)
        for tokens, filtered in zip(token_lists, df["tfidf_filtered_dialogue"], strict=True)
    ]
    analyzer = SentimentIntensityAnalyzer()

    def score(text: object) -> float:
        return np.nan if not isinstance(text, str) or not text.strip() else analyzer.polarity_scores(text)["compound"]

    # Reuse the supplied original/TF-IDF scores only after checking their fields;
    # calculate the new baseline with the same VADER implementation.
    if "sentiment_score" not in df or "tfidf_filtered_sentiment" not in df:
        raise ValueError("Supplied feature file lacks required VADER score columns")
    df["frequency_baseline_sentiment"] = df["frequency_baseline_dialogue"].map(score)
    keep = [
        "movie_id", "scene_number", "relative_position", "story_zone", "genre", "genre_list",
        "primary_genre", "sentiment_score", "tfidf_filtered_sentiment", "frequency_baseline_sentiment",
    ]
    out = intermediate_dir / "scene_features.pkl"
    df[keep].to_pickle(out)
    return out
