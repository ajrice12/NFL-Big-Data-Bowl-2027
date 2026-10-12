# NFL Big Data Bowl 2027

Starter analysis linking Combine movement to rookie regular-season NFL performance.
The project follows the requested `data`, `src`, `visualizations`, `outputs`,
`notebooks`, and `writeup` structure. Official data and generated outputs are
excluded from Git. No submission is published by these scripts.

## GitHub workspace

Repository: [ajrice12/NFL-Big-Data-Bowl-2027](https://github.com/ajrice12/NFL-Big-Data-Bowl-2027).
The private repository stores source code, the notebook, documentation, and the
writeup. `main` holds saved milestones; `codex/staging` is the working branch.
Official CSVs, processed Parquet, the Python environment, and generated outputs
remain local under the ignore rules. A clone requires downloading the official
competition data and rerunning the pipeline.

Save work from the staging branch:

```powershell
git add src visualizations notebooks writeup README.md requirements.txt .gitignore
git commit -m "Describe the analysis update"
git push
```

Review completed changes in a pull request from `codex/staging` into `main`.

## Setup

Run from this project directory with Python 3.11 or newer:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

This workspace also has a local `.venv` with PyArrow and access to the installed
system scientific packages. Run `.\.venv\Scripts\python.exe` in place of `python`
to use that environment. For a portable setup, use the requirements above.

## Pipeline

The supplied CSVs live in `data/raw/`. To import from another location, add
`--source "path/to/csv-folder"` to the ingestion command. Existing raw files are
preserved. Ingestion rewrites the selected processed Parquet files.

```powershell
python -m src.load_data
python -m src.clean_tracking
python -m src.combine_metrics
python -m src.nfl_outcomes
python -m src.validate_results
python -m src.train_models
python -m visualizations.statistical_figures
```

For the initial receiver model, ingestion needs only these tables; converting
game tracking is optional and may take several minutes:

```powershell
python -m src.load_data --tables players games combine_results combine_tracking player_play
```

`load_data.py` converts in batches; Combine cleaning and play outcomes load whole
tables into memory. Allow several GB of RAM for the full workflow. Large game
tracking files are converted but not consumed by the initial model. Raw `s`, `x`,
and `y` units remain source units until checked against the official dictionary.

## Analysis scope

`combine_metrics.py` measures speed, signed acceleration/deceleration, and duration
per attempt and drill. `nfl_outcomes.py` builds rookie WR/TE route separation with
explicit denominators and excludes preseason/postseason and nullified plays.
`train_models.py` compares traditional testing with additional tracking features,
using the latest draft cohort as a holdout. Defaults are exploratory, including
20 observed routes, 50% training feature availability, and fixed ridge alpha 10.
It saves predictions, model metrics, and paired player bootstrap uncertainty in
`outputs/results/`. It excludes career totals and draft selection from predictors.

The baseline still needs football-context adjustment and drill-specific hypotheses
before supporting scouting claims. See `writeup/draft.md` for limitations.

## Visualizations and notebook

```powershell
python -m visualizations.player_comparison --drill DRILL_NAME --players 12345 67890
python -m visualizations.movement_animation --event-id EVENT_ID --nfl-id 12345 --attempt 1
```

Use actual identifiers from `combine_attempt_metrics.parquet`. Animations assume
10 Hz playback; gaps are not interpolated. The notebook is a reproducible launcher
for this repository. On Kaggle, attach both the competition data and project code,
configure their paths in its setup cell, and review outputs before publishing.

Competition requirements in the draft are taken from the user-supplied excerpt,
not independently verified. The draft contains no invented results.
