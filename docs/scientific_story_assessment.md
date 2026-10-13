# Scientific question and presentation assessment

Assessment of `codex/staging`, starting at commit `64d8b27`.

## What the current experiment tests

The implemented OL model predicts each eligible rookie lineman's observed
any-pressure-allowed rate across eligible regular-season player-play proxy
opportunities. It compares traditional Combine measurements plus position
indicators with the same predictors plus median completed mirror recovery delay
and recovery completion fraction. Training uses earlier draft cohorts; the main
test holds out 2025 (37 training players, 17 test players, 54 eligible overall).
The target is a smoothed pressure-rate logit, fitted with fixed-penalty ridge
regression and transformed back to a rate. It is not an event-time model.

Traditional MAE is 2.3369 pressure-rate percentage points; with tracking it is
2.3929. Traditional minus tracking MAE is -0.0560 pp, with paired test-player
bootstrap 95% interval [-0.1881, 0.0715] pp. The small Brier improvement and worse
player MAE do not establish added predictive value. The training-rate-only
benchmark beats both on player MAE. Receiver separation remains a distinct study.

## What the title promises, and the mismatch

“The 3-Second Problem,” combined with “sustain pass protection,” implies a test
of protection through a specific time. The actual prediction target collapses
pressure across the observed dropback duration. A short clean play and a long
clean play both contribute a zero to that target. The model does not estimate
the chance an early-ending clean observation would remain clean at three seconds,
nor an individual blocker's causal ability to sustain protection.

Use **The Pass-Protection Test** for the implemented experiment. Keep three
seconds as a clearly labeled descriptive checkpoint, not a validated universal
cutoff or the model's prediction horizon.

## What the data can support now

`src/ol_outcomes.py` defines 23,768 eligible player-play proxy opportunities
among 81 rookies before model eligibility restrictions. These are not 23,768
unique NFL plays. The mutually exclusive time-checkpoint groups are:

| Classification | Count | Meaning |
|---|---:|---|
| Pressure by 3 s | 1,373 | Valid pressure time <=3 s, including exactly 3 s |
| Observed clean through 3 s | 8,833 | No pressure by the checkpoint and observed at least that long; includes later pressure |
| Ended before 3 s without pressure | 13,490 | Three-second outcome unobserved; not an established three-second success |
| Invalid/missing pressure timing | 72 | Excluded from time classification; still in the any-pressure outcome |

There are 2,202 pressure-allowed observations overall. Of these, 1,373 occur by
three seconds, 757 have valid times later than three seconds, and 72 have invalid
or missing timing. Thus “any pressure” is not a fourth disjoint time-checkpoint
group and must not be added to those groups. These counts reproduce the current
code and data, without creating a new fitted analysis. The clean-through group
includes the 757 later-pressure observations.

Long-dropback-only pressure rates describe a selected set of observed durations;
they do not correct informative release censoring. Neither those rates nor the
checkpoint counts establish causal blocker quality. Player assignment, scheme,
QB behavior, rusher quality, units and label semantics need further validation.

## Presentation changes authorized without new science

1. Show an explicitly illustrative OL/rusher/QB diagram and the football problem.
2. Put the verified negative/inconclusive finding immediately after the opener.
3. Explain the three observation endings using illustrative timelines alongside
   source-derived counts. Label three seconds as a chosen descriptive checkpoint.
4. Connect mirror recovery to reacting to a rusher's change of direction as a
   hypothesis, while noting the drill omits contact, assignments and QB context.
5. Render actual Combine coordinates on a practice-drill grid with schematic
   equipment outside the trace, not on a 100-yard game field. Never invent an
   opponent trajectory or label equipment placement as measured.
6. Keep the full metric, PCA, filtering, coefficients and diagnostics in Research
   Tools; make the extra measurement scene optional.

## Separate proposal: a true three-second study (not implemented)

Prespecify the question and estimand before fitting. Validate pressure and release
timestamps and eligible assignments. Decide whether to predict observed
three-second status, an event-time distribution, or another explicit outcome.
Audit the effect of release/end-of-dropback censoring; a survival model alone
does not solve informative censoring. Do not relabel early clean endings as
three-second successes or silently drop them and claim an unconditional effect.
Design temporal validation, calibration, simple benchmarks, sensitivity to
censoring assumptions and uncertainty with player/game dependence and model
refitting. Report as a separate experiment. No existing model was changed here.

## Football context sources

NFL Next Gen Stats exposes time to throw as a measure of release timing:
https://nextgenstats.nfl.com/stats/passing/2026/REG/1 . This supports explaining
why observation duration matters; it does not validate a universal three-second
blocking standard. NFL Combine reporting discusses lateral foot quickness as
scouting context: https://www.nfl.com/news/2025-nfl-combine-stock-up-stock-down-day-4 .
The present study's recovery-to-pressure link remains a hypothesis, not an NFL
endorsed measurement.

The sixty-second comprehension review is an editorial walkthrough, not a human
participant study. See the verification record for what was actually tested.
