# Do Genres Feel Different? Reproducible Movie-Dialogue Analysis

## Research questions

1. Do movie genres create distinct emotional arcs through dialogue?
2. Where in a film's story structure do genres differ most in sentiment?
3. Does genre-specific vocabulary carry stronger emotional tone than ordinary dialogue?

## Data source

The screenplay source is **Film Corpus 2.0**, described by its publishers as a corpus of 960 screenplays. The supplied processing log, however, contains 1,070 unique candidate file IDs. This discrepancy must be resolved against the original download before publication; this repository reports both numbers and never silently uses 960 as the processing denominator.

Movie title, runtime, and genre metadata came from TMDb. TMDb data is not an external validation set: it is metadata joined by automated title matching.

Raw Film Corpus files are not redistributed here. Place the supplied CSV exports in `data/raw/` or pass their directory with `--data-dir`.

## Analyses and interpretation

The main genre arc is the mean of film-level story-zone means. Confidence intervals resample films, not scenes. Figure labels show the number of unique films contributing to each genre.

The dialogue-method comparison includes:

- VADER on full scene dialogue;
- VADER on the supplied TF-IDF-filtered dialogue;
- VADER on a simple baseline consisting of the highest-corpus-frequency non-stopword tokens in each scene, matched to the TF-IDF text's retained-token count.

The genre sensitivity table compares TMDb's first listed genre (primary genre) with a multi-label analysis in which a film contributes once to every listed genre. These estimates answer different questions and should be shown together.

No predictive model is part of the final workflow. If one is added later, use `GroupShuffleSplit`, `GroupKFold`, or an equivalent split with `movie_id` as the group. Scenes from one screenplay must never appear in both training and test data.

## Limitations

- VADER was designed for general social text, not specifically for screenplay dialogue.
- Screenplays vary substantially in formatting, and the parser recognizes only a limited set of scene-heading and dialogue conventions.
- Automated TMDb title matching can select the wrong film, especially for remakes, reordered articles, sequels, and short titles.
- Genre labels overlap; primary-genre and multi-label estimates have different interpretations.
- Genre sample sizes are unequal. Per-film aggregation and film-level confidence intervals reduce, but do not eliminate, this limitation.
- The TF-IDF and baseline scores are transformations of the same dialogue as the full-text score. Their correlations measure association, not external validity.
- The supplied log/corpus-size discrepancy (1,070 versus 960) remains a provenance issue until checked against the original corpus download.

TMDb is used as a metadata source; this project is not endorsed or certified by TMDb.
