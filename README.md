# Do Genres Feel Different? Reproducible Movie-Dialogue Analysis

This repository rebuilds the DATASCI 112 final project as six explicit stages and adds the robustness checks needed before the project is linked publicly.

## Research questions

1. Do movie genres create distinct emotional arcs through dialogue?
2. Where in a film's story structure do genres differ most in sentiment?
3. Does genre-specific vocabulary carry stronger emotional tone than ordinary dialogue?

## Data source

The screenplay source is **Film Corpus 2.0**, described by its publishers as a corpus of 960 screenplays. The supplied processing log, however, contains 1,070 unique candidate file IDs. This discrepancy must be resolved against the original download before publication; this repository reports both numbers and never silently uses 960 as the processing denominator.

Movie title, runtime, and genre metadata came from TMDb. TMDb data is not an external validation set: it is metadata joined by automated title matching.

Raw Film Corpus files are not redistributed here. Place the supplied CSV exports in `data/raw/` or pass their directory with `--data-dir`.

## Workflow

1. `src/01_data_acquisition.py` inventories the supplied corpus artifacts and records the source-count discrepancy.
2. `src/02_script_parsing.py` audits screenplay parsing outcomes.
3. `src/03_tmdb_matching.py` audits matched, unmatched, and ambiguous titles. Matches with `title_score < 90` are ambiguous by the preregistered default and are excluded from the main analysis.
4. `src/04_feature_construction.py` assigns story zones, calculates full-dialogue VADER, preserves the supplied TF-IDF-filtered comparison, and constructs a frequency-token baseline using the same number of retained tokens per scene.
5. `src/05_analysis.py` aggregates scenes within film before genre comparisons, creates 95% film-level bootstrap intervals, and runs both primary-genre and multi-label analyses.
6. `src/06_figure_generation.py` draws final figures with film counts and uncertainty intervals.

This ordering prevents scenes from long scripts from receiving more weight than scenes from short scripts in genre-level estimates.

## Reproduce

Use Python 3.11 or newer from a clean environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python reproduce.py --data-dir data/raw --bootstrap 2000 --seed 112
```

For Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`. The single command writes audit tables to `results/reports/`, analysis tables to `results/tables/`, and PNG/PDF figures to `results/figures/`.

The supplied archive must contain at least:

- `scene_extraction_log.csv`
- `tmdb_api_movie_metadata.csv`
- `tmdb_api_unmatched_movies.csv`
- `scene_level_tfidf_filtered_sentiment.csv`

## Quality-control rules and sample flow

`results/reports/sample_flow.csv` is the source of truth. In the supplied exports:

- Film Corpus 2.0 published corpus size: **960**
- Candidate IDs in the supplied extraction log: **1,070**
- Parsed: **685**
- Parsing failures: **385** (263 with no recognized scene headings; 122 missing a scene-only file)
- TMDb matched: **597**
- TMDb unmatched: **88**
- Ambiguous matches (`title_score < 90`): **75**
- High-confidence matches eligible for the main analysis: **522** before later missing-data exclusions

The ambiguous threshold is deliberately conservative and easy to audit. A human should review `results/reports/ambiguous_tmdb_matches.csv`; changing the threshold is a sensitivity decision and must be reported.

## Analyses and interpretation

The main genre arc is the mean of film-level story-zone means. Confidence intervals resample films, not scenes. Figure labels show the number of unique films contributing to each genre.

The dialogue-method comparison includes:

- VADER on full scene dialogue;
- VADER on the supplied TF-IDF-filtered dialogue;
- VADER on a simple baseline consisting of the highest-corpus-frequency non-stopword tokens in each scene, matched to the TF-IDF text's retained-token count.

The genre sensitivity table compares TMDb's first listed genre (primary genre) with a multi-label analysis in which a film contributes once to every listed genre. These estimates answer different questions and should be shown together.

No predictive model is part of the final workflow. If one is added later, use `GroupShuffleSplit`, `GroupKFold`, or an equivalent split with `movie_id` as the group. Scenes from one screenplay must never appear in both training and test data.

## Results

Run the pipeline before writing result prose. `results/reports/findings.md` is generated from the corrected outputs and is the only approved source for poster/application claims. The original poster's scene-level correlation (`r = 0.79`) is an association between two transformations of the same dialogue; it is not external validation. It must not be described as proof that TF-IDF preserves a validated emotional signal.

The original poster is retained only as a historical source. Update it if the regenerated high-confidence, per-film results differ.

## Limitations

- VADER was designed for general social text, not specifically for screenplay dialogue.
- Screenplays vary substantially in formatting, and the parser recognizes only a limited set of scene-heading and dialogue conventions.
- Automated TMDb title matching can select the wrong film, especially for remakes, reordered articles, sequels, and short titles.
- Genre labels overlap; primary-genre and multi-label estimates have different interpretations.
- Genre sample sizes are unequal. Per-film aggregation and film-level confidence intervals reduce, but do not eliminate, this limitation.
- The TF-IDF and baseline scores are transformations of the same dialogue as the full-text score. Their correlations measure association, not external validity.
- The supplied log/corpus-size discrepancy (1,070 versus 960) remains a provenance issue until checked against the original corpus download.

## Division of work

The submitted files name Miller Roberts and Hannah Zingapan but contain no authorship metadata or contribution record. An exact division of work therefore cannot be reconstructed responsibly from the files. Before publishing, both authors must replace this section with a jointly confirmed statement covering data acquisition, parsing, TMDb matching, analysis, visualization, poster writing, and final verification. Do not invent attribution for an application.

Suggested confirmation table:

| Work item | Miller Roberts | Hannah Zingapan |
|---|---|---|
| Data acquisition and corpus organization | Confirm | Confirm |
| Script parser and extraction audit | Confirm | Confirm |
| TMDb matching and manual review | Confirm | Confirm |
| Feature construction and VADER/TF-IDF methods | Confirm | Confirm |
| Statistical analysis and robustness checks | Confirm | Confirm |
| Figures, poster, and written interpretation | Confirm | Confirm |

## Public-release checklist

- Confirm the exact contribution statement with both authors.
- Resolve the 960-versus-1,070 corpus discrepancy.
- Manually adjudicate ambiguous TMDb matches.
- Run the clean-environment command above.
- Compare generated findings with every poster/application sentence and revise unsupported claims.
- Confirm there are no API tokens, raw restricted scripts, or files over GitHub's limits.
- Make the repository public only after these checks, then test the public clone instructions once more.

TMDb is used as a metadata source; this project is not endorsed or certified by TMDb.
