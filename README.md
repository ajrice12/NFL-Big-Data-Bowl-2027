# The 3-Second Problem

Can Combine movement mechanics reveal which offensive linemen sustain pass protection under pressure?

A local research presentation, movement laboratory, and reproducible analysis for
NFL Big Data Bowl 2027. The public [GitHub repository](https://github.com/ajrice12/NFL-Big-Data-Bowl-2027)
stores code and documentation. `codex/staging` contains development work; `main`
contains earlier milestones. This is independent exploratory research, with no
NFL endorsement or validated scouting score.

## View the presentation

From the project root, after generating the analysis export:

```powershell
.\.venv\Scripts\python.exe -m scripts.serve --port 8765
```

Open **http://127.0.0.1:8765/presentation/** on this computer. Keep the terminal
running; Ctrl+C stops it. The server binds only to loopback and serves only
presentation assets and generated research figures/animation/export. It refuses
raw CSV requests. Opening HTML by double-clicking does not provide the HTTP
module/data loading the app needs. The old inline-preview scripts are archived
under `scripts/legacy/` and are not the application entry point.

Five sections form a short research briefing: **Overview, Player movement,
How the metric works, Findings, and NFL application**. The first screen shows the
question, candidate metric, 54-player model cohort, 21,363 NFL proxy opportunities,
17 held-out athletes, and the inconclusive added-value finding beside actual
Combine movement.

The field viewer uses an original code-drawn football practice field, compact
player labels and live speed/acceleration readouts. Compare two real attempts in
overlay or side by side. Play/pause, replay, scrub time, change speed, select drills,
and inspect reversal/recovery markers and the synchronized speed chart. Rookie
NFL rates and explicit opportunity denominators appear directly alongside film.
The Metric section steps through an observed reversal and its recovery target;
15%, 20% and 25% definitions use actual exported measurements.

Field markings are **schematic**, not recorded NFL field placement. Coordinate
units remain unverified. A source-unit scale bar and shared isotropic mapping
preserve geometry; starts are translated, never rotated or interpolated. Gaps
break trails. NFL outcomes are descriptive and do not validate the movement score.
Detailed samples and nine-method explanations are secondary expandable appendices.

Startup reads a 24.8 KB `briefing.json` and the two featured attempts, not all 480
trajectories. `catalog.json` loads when entering Movement; individual attempt
files load only when selected and are reused in memory. Missing briefing, model
outputs or selected attempts show explicit incomplete/unavailable states. Previous
chapter URLs such as `#laboratory` redirect to the corresponding new section.

## Setup and reproduce

Python 3.11+ and several GB of RAM are recommended. Obtain the official dataset
through authorized competition access. Original data is not supplied in Git.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.load_data --source "C:\path\to\official-csv-folder" --tables players games combine_results combine_tracking player_play
python -m src.clean_tracking
python -m src.combine_metrics
python -m src.nfl_outcomes
python -m src.validate_results
python -m src.train_models
python -m src.ol_movement
python -m src.ol_outcomes
python -m src.ol_models
python -m src.ol_sensitivity
python -m scripts.research_checks
python -m scripts.build_presentation
python -m scripts.verify_presentation_export
python -m visualizations.research_figures
python -m visualizations.comparison_export
python -m scripts.serve --port 8765
```

Only five CSVs are required for the analyses. `python -m src.load_data` converts
all local CSVs, including optional game tracking. Ingestion is batched; feature
and outcome construction load selected tables in memory. Existing raw files
are preserved; derived files are regenerated. The local workspace environment
has system scientific packages enabled; use a fresh venv and requirements for a
portable installation.

## Separate experiments and verified findings

| Experiment | Earlier training / 2025 test players | Traditional MAE | Tracking MAE |
|---|---:|---:|---:|
| OL any-pressure rate | 37 / 17 | 0.0233688 | 0.0239290 |
| WR/TE mean receiving separation | 67 / 27 | 0.249064 | 0.543811 |

OL errors are pressure-rate fractions. Receiver errors use source separation
units. Receiver scores never validate the OL hypothesis. Both models use
training-only preprocessing and fixed ridge regularization, with distinct
features and targets. See `docs/research_protocol.md` for exact definitions.

The candidate Lateral Reset Efficiency feature is median completed recovery
delay after a detected mirror reversal, using a geometric axis proxy and a
20% robust-excursion target. It is **not validated**. In the OL holdout,
traditional minus tracking MAE is −0.0005602, with paired test-player bootstrap
95% interval [−0.0018807, 0.0007150]. Both models lose to the pooled training-rate
benchmark (MAE 0.0212205). Opportunity-weighted Brier very slightly favors
tracking (0.0823834 versus 0.0823928). No independent repeated mirror attempts
are available. Earlier temporal splits and 15%/25% target sensitivity are shown.

There are 23,768 proxy OL protection opportunities, not independently validated
blocking assignments. Of these, 1,373 have pressure by three seconds, 8,833 are
observed clean through three seconds, 13,490 are censored earlier, and 72 have
invalid/missing timing. Binary-rate models retain the independently valid
opportunities. Formal survival prediction is deferred because releases can be
informative censoring. Scheme, quarterback behavior and deployment remain
uncontrolled. Run-in/run-out phases are not separately identified and may
influence the dominant movement axis and excursion.

## Verification

```powershell
python -m unittest discover -s tests -p "test_*.py"
python -m scripts.research_checks
python -m scripts.build_notebook
python -m scripts.verify_notebook
```

For browser checks, install Node.js and Playwright outside the Python venv:

```powershell
npm install --no-save playwright
node tests/browser.cjs
```

Start the local server first. The browser test defaults to installed Windows
Edge. Set `BROWSER_EXECUTABLE` to another Chromium executable,
`PLAYWRIGHT_MODULE_PATH` to an existing Playwright module, and
`PRESENTATION_URL` to override the test URL. It writes its actual status and
screenshots to `outputs/verification/`. A failed check exits nonzero. The suite
covers all five sections, playback/pause/scrub/replay, athletes/drills, data samples,
metric event/target controls, both result hypotheses, desktop/laptop/mobile overflow,
on-demand loading, missing briefing/model/attempt handling,
console/resource errors, and refusal to serve original CSVs.

`verify_notebook` executes the embedded code in a fresh local reproduction
directory. It does not claim execution on Kaggle's runtime. The maintained
notebook embeds required source modules and finds the official attached dataset
without downloading the repository. Rebuild it after source changes. Its final
Kaggle cleanup removes reconstructable data/export/prediction files from the
public output bundle; review allowed figures and competition rules separately.

## Project map and outputs

- `src/`: ingestion, cleaning, receiver experiment, OL movement/outcomes/models/sensitivity.
- `presentation/`: modular HTML/CSS/JS; no embedded tracking records.
- `scripts/`: local export, server, independent checks, notebook generation/verification.
- `visualizations/`: original visualizations plus scientific figures and comparison GIF.
- `notebooks/kaggle_submission.ipynb`: self-contained, output-free reproduction notebook.
- `docs/technical_audit.md`: development checkpoint, original defects and changes.
- `docs/research_protocol.md`: operational definitions, assumptions and validation design.
- `docs/redesign_review.md`: presentation audit, five-section design and verification.
- `writeup/draft.md`: concise scientific Writeup draft with five figure references.

Generated files remain local and ignored: `outputs/research/` holds analysis
reports; `outputs/presentation/` contains restricted local exports (`briefing.json`,
`catalog.json`, `appendix.json`, individual `attempts/` files, and the retained
full `research.json` for scientific exporters); `outputs/figures/` contains five 240-dpi PNG/SVG figures;
`outputs/animations/mirror_comparison.gif` is a 10-fps real-frame comparison;
`outputs/verification/` contains checks, screenshots and execution logs. Earlier
results/presentation are preserved in `outputs/checkpoints/pre-overhaul/` and Git
history. Historical custom builders were moved out of `.venv/` into
`scripts/legacy/`; they are not maintained or portable entry points.

## Publication boundary

Do not commit or deploy raw competition CSVs, processed tracking, local trajectory
exports, or animation/screenshot assets that reconstruct restricted data. The
public repository contains source, aggregate written findings and the unexecuted
notebook. Current license/dictionary text could not be retrieved during this
session; coordinate units and sharing permissions need verification before a
competition publication. The draft uses the supplied excerpt's ≤2,000-word and
fewer-than-10-table/figure limits; this is not a submitted Kaggle entry.
