# Two experiments, separate evidence

## Receiver separation (existing)

The original ridge model and its outputs are preserved. The latest cohort
holdout is the principal receiver finding. It does not validate offensive-line
pass protection. Added tracking worsens its initial prediction error.

## Offensive line: candidate Lateral Reset Efficiency

This implementation is an exploratory operational definition, selected before
running the OL model. No validated scouting score is asserted.

1. Retain C/G/T prospects and normalize the two mirror-drill name spellings.
2. Order actual PLAYER frames by timestamp. Compute derivatives only between
   finite frames with 0.05–0.15 seconds elapsed. Gaps start independent segments.
3. Center each attempt's x/y coordinates and take its first principal component
   as a dominant movement axis. This is a **lateral proxy**, pending dictionary
   and drill-orientation validation. Report the explained variance fraction.
4. Compute signed axis velocity from successive observed displacements. A
   centered three-frame rolling median stabilizes reversal detection only.
   Coordinates and displayed trajectories are never smoothed.
5. Require at least three samples with the same nonzero sign before and after
   a reversal. Suppress samples below 10% of the attempt's 90th percentile
   absolute axis velocity. Use the extremal observed coordinate between runs
   as the reversal frame. Collapse same-direction duplicate detections.
6. Following each reversal, measure time until the player moves 20% of the
   attempt's 90th–10th percentile axis excursion in the new direction. Stop at
   the next reversal, a gap, or attempt end. Unreached targets are censored.
   No sub-frame time or missing coordinate is interpolated.
7. Use median **completed** recovery delay and completion fraction as separate
   athlete features. Shorter delay is the hypothesized direction of efficiency.
   Do not call the median unbiased when incompletions differ. Include unresolved
   events in the completion denominator and show sensitivity at 15% and 25%.

Within-attempt odd/even event agreement is descriptive, not repeated-attempt
reliability. If no independent repeated attempts exist, report repeatability as
unresolved. An absence of usable reversals is missing data, not zero delay.

## NFL outcomes and comparisons

Use rookie regular-season non-nullified rows, actual lined-up C/G/T role,
known pressure flag, positive dropback duration, and ≥1 recorded rusher encountered.
These are **proxy pass-protection opportunities** based on supplied fields,
not independently verified blocking assignments. Define any-pressure rate from
all such opportunities and conditional long-dropback pressure rate among
dropbacks ≥3 seconds. Denominators always accompany rates.

For three-second descriptive risk sets, a player is observed pressure-free at
3 seconds only when observation lasts at least 3 seconds. Pressure before 3
seconds is an event. Earlier endings without pressure are censored/unknown.
Exclude inconsistent event times from timing summaries, retaining independently
valid binary opportunities. A Kaplan–Meier curve would be a descriptive reference
whose independent-censoring assumption can fail because releases and pressure
affect each other. It is not implemented here; formal survival modeling is deferred.

Primary OL models predict athlete rookie pressure rate, requiring ≥50 proxy
opportunities. Compare traditional tests plus C/G/T role with those same fields
plus candidate recovery delay and completion fraction. Fit ridge alpha 10 to
Jeffreys-smoothed logit rates; imputation/scaling fit only on earlier cohorts.
Keep all players from the latest draft cohort held out. Report player MAE,
opportunity-weighted Brier score, and paired test-player bootstrap intervals.
Use fixed hyperparameters to avoid tuning on the holdout. Evaluate the 2024 and
2025 temporal splits where sample sizes permit. Effects describe standardized
ridge coefficients, not causality or significance.

Case studies: within the most common eligible OL position, choose the players
nearest the 25th, 50th, and 75th recovery-delay percentiles, breaking ties by ID.
Use only adequate-opportunity athletes. Selection does not inspect outcomes.
Examples are descriptive, regardless of whether a player is in the holdout.

Competition limits are taken from the supplied excerpt (≤2,000 words and <10
tables/figures). Current license and submission rules require final review.
The application is local-only. Exported raw examples stay ignored and unhosted.


Run-in/run-out phases are not labeled or cropped in the present implementation.
They can influence the PCA axis and excursion target. Football-lateral validity
requires drill-phase/orientation review before a scouting interpretation.
