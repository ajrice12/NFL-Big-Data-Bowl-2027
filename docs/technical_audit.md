# Technical audit before overhaul

Checkpoint: `cc9cae6`. The ignored local outputs and last inline presentation were
copied into `outputs/checkpoints/pre-overhaul/` before research changes.

## Existing evidence

The original experiment predicts rookie WR/TE mean receiving separation on
non-nullified regular-season routes. It joins by player and draft year, requires
20 observed separation values, and holds out the latest draft cohort. It fits
median imputation and standardization on training players only, then ridge models
with fixed alpha 10. The enhanced model includes many drill-specific sensor
features passing 50% training availability. This is a broad exploratory model.

Its outputs exist locally: `model_comparison.json`, `held_out_predictions.csv`,
`validation.txt`, two PNGs, and one short GIF. Re-running the original trainer
reproduced 67 training players, 27 held-out 2025 players, baseline MAE 0.2490636,
tracking MAE 0.5438110, and a paired bootstrap MAE improvement of -0.2947474
(95% interval -0.5047408 to -0.1024340). These are receiver results only.

## Foundational issues

- The validation script checks keys and simple ranges but does not independently
  recheck every season/opportunity exclusion. Its original docstring overstates
  cohort validation. It does not test held-out model leakage or censoring.
- IDs are stored as nullable floats by ingestion. Values fit exactly, but explicit
  integer validation is needed before joins and presentation exports.
- Cleaning removes invalid rows and duplicates but does not report conflicting
  duplicates, gap coverage, nonfinite coordinates, or acceleration quality.
- Attempt metrics summarize all frames, including stationary periods. No
  directional reversal, lateral-axis definition, or gap-aware recovery exists.
- Ridge regularization is fixed, context adjustment is absent, and the bootstrap
  reflects test-player sampling only. R² is negative for the enhanced model.
- The notebook requires an external project checkout and has no OL analysis.
- The draft says results are not generated although results exist.
- README visibility is stale: GitHub was subsequently made public.

## Presentation defects and scope

The initial presentation ran in one HTML fragment, with data and logic embedded.
It repeatedly failed in the chat renderer even though the local wrapper passed.
Changing JSON loading did not establish the actual host failure cause. The final
fallback uses native CSS animation without a startup script. It shows genuine
coordinate paths but lacks synchronized comparisons, scrub controls, moving
speed charts, algorithm explanations, and a reproducible application build.
The original GIF assumes fixed 10 Hz playback rather than checking timestamps.

Three custom build scripts and an intermediate JSON export were found inside
`.venv/`. Source scripts have been moved to `scripts/legacy/`. They are deprecated
historical files, not the new build path. The old raw inline JSON is archived only
in ignored local outputs. No existing analysis has been relabeled as OL evidence.

## OL feasibility

Player metadata contains 121 C/G/T prospects. Preliminary screening found 42,684
rookie regular-season non-nullified OL player-play rows for 84 players; 25,017
have both pressure flags and dropback duration. These counts precede strict role,
rusher, timing, and opportunity exclusions. Two spellings identify mirror drills:
`PASS_PRO-MIRROR_DRILL` and `PASS_PRO_MIRROR_DRILL`. They must be normalized.
Mirror tracking has 121 attempts in total, so independent repeated-attempt
reliability may be unavailable. The build will report this rather than invent it.

The coordinate dictionary and the competition license are not present locally.
Distances and speeds retain source units. A dominant-axis displacement can serve
as an explicitly provisional lateral proxy, not anatomically verified lateral
motion. Dropback end is potentially informative censoring, so short clean plays
cannot establish sustained three-second protection. Formal survival prediction
requires further validation of timing and censoring assumptions.

## Overhaul requirements

Keep receiver and OL artifacts in distinct paths. Export raw trajectories only
to ignored local files. Build a modular local HTTP presentation with explicit
loading/error states and eight chapters. Test its real browser behavior and save
screenshots. Public source may contain code, aggregate summaries, and methods;
it must not contain original CSVs or reconstructable frame exports.

## Implemented and verified overhaul

The preserved receiver outputs reproduce exactly. New OL modules construct
mirror features, proxy NFL opportunities, temporal pressure-rate models and
threshold sensitivity without reusing receiver evidence. The final strict cohort
has 23,768 opportunities / 81 athletes and a 54-player modeling cohort. The
primary holdout has 37 training and 17 test players. Candidate LRE does not
establish incremental predictive value. There are no independent repeated
mirror attempts; a survival prediction model is deliberately deferred.

Cleaning now rejects nonfinite geometry/speed, validates integer-valued keys,
reports conflicting duplicate timestamps and invalid derivative intervals, and
preserves the original first-row duplicate policy. In the supplied data there
are zero conflicting duplicates, invalid geometry/speed rows, or invalid
within-attempt derivative intervals among 431,094 retained PLAYER frames.
The original validator's overstated docstring was corrected; independent cohort
and censoring checks now live in `scripts/research_checks.py`.

The modular local HTTP app replaces reliance on the unsupported inline host.
Its schema check, missing-export message, whitelisted loopback server, and
browser checks address the observable failure modes. The original chat-host
failure remains undiagnosed; no claim is made that its internal cause was fixed.
Testing caught and repaired a sample export format mismatch and mobile selector
overflow. The app now passes 33 browser checks with zero execution/console
errors or failed application resource requests. Five chapter screenshots and a
mobile screenshot are saved locally. Browser tests use actual Edge/Playwright.

Eight research edge-case tests and ten output/cohort checks pass. Eight notebook
code cells execute in a fresh local reproduction directory; five full analysis
reports match the workspace exactly. Kaggle runtime execution is not claimed.
Five scientific PNG/SVG figures and a real-frame comparison GIF are generated.
The Writeup draft has five figure references and fewer than 2,000 words.

The presentation includes actual trajectories only through an ignored local
export. Raw data, processed records, generated animations/screenshots/figures,
and notebook reproduction directories remain excluded from the public source.
Current competition rules/dictionary retrieval did not return usable text;
source units and publication permissions remain unverified. Run-in/run-out
phases are not segmented and can influence the dominant-axis proxy. These are
explicit scientific/publication limitations, not evidence of metric validity.
