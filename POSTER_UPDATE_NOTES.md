# Poster and application update notes

The supplied poster is a historical artifact. Its conclusions should not be reused unchanged.

## Claims that remain numerically reproducible

- The original scene-level full-dialogue versus TF-IDF-filtered VADER correlation is approximately `r = 0.79` in the corrected high-confidence subset (`r = 0.793`).
- In the eight largest primary genres, Comedy remains comparatively positive across the story and Horror has the most negative resolution.

## Claims that need qualification or replacement

- Replace “TF-IDF filtering preserved emotional signal” with: “Full-dialogue and TF-IDF-filtered VADER scores were associated (`r = 0.793`), but a matched-length frequency-token baseline was also strongly associated (`r = 0.744`); neither comparison is external validation.”
- Do not claim that the correlation alone proves genre-specific vocabulary has stronger emotional tone.
- Replace scene-weighted genre arcs with film-weighted arcs and show 95% film-bootstrap intervals plus film counts.
- State that primary-genre and multi-label results differ for some genre-zone estimates; consult `genre_assignment_sensitivity.csv`.
- Report the complete sample flow: 1,070 logged candidates, 685 parsed, 597 automatically matched, 88 unmatched, 75 ambiguous under the default threshold, 522 high-confidence eligible films, and 515 films in the complete three-method comparison.
- Do not say “of 960 scripts” survived without explaining why the supplied extraction log contains 1,070 candidate IDs.

## Suggested replacement conclusion

After aggregating scenes within films and excluding low-confidence TMDb matches, the largest genres retained different average dialogue-sentiment trajectories, but uncertainty intervals overlapped for many comparisons. Comedy was comparatively positive across story zones, while Horror had the most negative resolution among the eight largest primary genres. Full-dialogue and TF-IDF-filtered VADER scores were associated, but a simple matched-length frequency-token baseline was also strongly associated, so the analysis does not establish that TF-IDF-selected vocabulary uniquely preserves emotional information. Genre estimates were sensitive in some cases to whether films used only their primary genre or all TMDb genres. These findings are descriptive and do not validate VADER for screenplay dialogue.
