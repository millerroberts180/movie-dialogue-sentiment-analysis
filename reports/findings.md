# Generated findings

This file was generated from the high-confidence (`title_score >= 90`) analysis.

- Parsed 685 of 1070 IDs in the supplied extraction log; the publisher-described corpus size is 960 and the discrepancy requires resolution.
- TMDb returned 597 matches and 88 unmatched titles; 75 matches were flagged as ambiguous, leaving 522 eligible films before missing-data exclusions.
- The complete three-method comparison contains 44556 scenes from 515 films.
- The scene-level association between full-dialogue and TF-IDF-filtered VADER is r = 0.793. The corresponding frequency-baseline association is r = 0.744. Because the baseline is also strongly associated, `r = 0.79` does not by itself establish a special genre-vocabulary effect. These are associations between transformations of the same text, not external validation.
- Genre claims must be read from `genre_arcs_with_film_bootstrap_ci.csv`, which uses equal film weighting and film-level 95% bootstrap intervals. In the eight largest primary genres, Comedy is the most positive throughout and Horror has the most negative resolution; uncertainty bands overlap for many other comparisons.
- Primary-genre sensitivity is reported beside the multi-label estimates in `genre_assignment_sensitivity.csv`. The mean absolute change across genre-zone estimates is 0.067, with a maximum of 0.353; genre-assignment choice can therefore materially affect individual estimates.
