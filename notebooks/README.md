# Notebook migration note

The two submitted Colab notebooks are retained in `legacy/` for provenance. They are not the reproducible entry point because they contain Google Drive-specific paths, inline package installation, and extraction/TMDb operations combined in single notebooks.

The tested workflow is the six-stage script sequence invoked by `python reproduce.py`. Raw screenplay files were not included in the supplied archive, so stages 1-3 audit the saved acquisition, parsing, and matching artifacts. Re-running raw extraction requires the original Film Corpus 2.0 `full_scripts/` and `scene_only/` directories. Re-running live TMDb matching additionally requires a bearer token supplied through an environment variable; no token belongs in a notebook or repository.
