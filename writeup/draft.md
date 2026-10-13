# The Pass-Protection Test

**Does Combine mirror recovery add information when predicting overall rookie pressure allowed?**

## Research question

Traditional Combine tests compress performance into a time, distance or jump.
Mirror drills expose transitions: moving, reversing, and recovering displacement.
We investigate whether an exploratory recovery feature adds predictive information
about rookie offensive-line pressure rates beyond traditional tests. We also
preserve an existing, separate receiver-separation experiment. Neither experiment
establishes a validated scouting score. The OL target is overall pressure-allowed rate, not protection lasting three seconds.

## Data and feasibility

The supplied dataset contains 510 prospects, 463,189 Combine tracking rows,
314,197 NFL player-play rows and 1,002 games. Cleaning retains 431,094 PLAYER
frames across 6,310 Combine attempts. The three game-tracking files contain
22,654,290 rows, but this analysis uses player-play outcomes rather than
reconstructing blocking assignments from game coordinates.

Among 121 offensive linemen with mirror tracking, 118 have defined completed
recovery delays. Each has only one mirror attempt. Independent repeated-attempt
reliability therefore cannot be tested. Rookie regular-season OL records yield
23,768 proxy protection opportunities across 81 athletes. Joining traditional
measurements and mirror features, requiring at least 50 opportunities and at
least two detected reversals, leaves 54 model players.

This supports an exploratory feasibility test, not a reliable prospect ranking.
The receiver experiment has more held-out players but tests a different football
question; its model scores cannot be transferred to pass protection.

## Candidate measurement

Frames are ordered within player, draft year, event, drill and attempt. Missing or
nonfinite coordinates, invalid speed, and duplicate timestamps are rejected or
reported. Derivatives use intervals of 0.05–0.15 seconds; gaps form independent
segments. No missing trajectory is interpolated.

Centered x/y coordinates are projected onto the first principal component, with
a deterministic sign. This dominant-axis projection is a **lateral proxy**; body
orientation is unavailable. A centered three-frame median stabilizes axis velocity
for reversal detection only. Opposite nonzero sign runs must each last at least
three frames above 10% of the attempt's 90th-percentile absolute axis velocity.
The observed coordinate extremum between runs identifies the reversal.

The displacement target is 20% of within-attempt p90–p10 projected excursion.
Recovery delay is elapsed time to the first recorded frame reaching that target
in the new direction, before the next reversal, a gap or attempt end. Unreached
targets remain censored. Median completed delay and completion fraction enter the
model separately. Smaller delay is the hypothesized direction of efficiency,
not a validated interpretation.

There are 472 detected reversals and 458 completed recoveries. Odd/even completed
reversal medians correlate descriptively (Spearman 0.758, 88 players), but events
within one attempt share conditions and do not establish repeatability. Unlabeled
run-in/run-out phases may influence the axis and excursion. Targets at 15% and
25% audit definition sensitivity rather than select a held-out winner.

![Figure 1. Actual projected mirror movement and observed recovery intervals.](../outputs/figures/lre_worked_example.png)

## NFL observation and censoring

Proxy opportunities require rookie regular-season, non-nullified player-play
records, C/G/T lineup position, a known pressure flag, positive dropback duration,
at least one encountered rusher and a recorded pass result. These rules do not
independently verify blocking assignments or individual responsibility.

We retain binary pressure outcomes while separately validating pressure timing.
At three seconds, 1,373 observations have experienced pressure, 8,833 are observed
clean through the threshold, 13,490 are censored earlier, and 72 have inconsistent
or missing timing. A later pressure still permits an observed clean state at
three seconds. A short pressure-free dropback provides no evidence about the
unobserved remainder.

Any-pressure rates by observed duration are descriptive and conditional. Release,
quarterback behavior, opponent, scheme and deployment may affect both duration
and pressure. Formal time-to-event prediction is deferred: independent censoring
is not established. The primary model predicts player any-pressure rate, not a
three-second survival hazard.

![Figure 2. Timing classifications and conditional pressure rates.](../outputs/figures/nfl_observation_boundary.png)

## Model and validation

The baseline uses height, weight, ten-yard split, forty, vertical jump, broad
jump, three-cone, short shuttle and position indicators. The tracking model adds
only mirror recovery delay and completion fraction. Ridge regression with fixed
alpha 10 predicts Jeffreys-smoothed logit pressure rates. Imputation and scaling
fit only earlier draft cohorts. Players receive equal training weight.

The primary split trains on 37 earlier-cohort players and tests on 17 players
from 2025, representing 14,844 training and 6,519 test opportunities. We report
player MAE and opportunity-weighted binary Brier score. Paired bootstrap
resampling of 2,000 held-out player samples estimates uncertainty in traditional
minus tracking MAE. This conditions on fitted models and omits training-refit
uncertainty and game clustering.

## Findings

Traditional OL MAE is **0.023369**; tracking MAE is **0.023929**. The improvement
is **−0.000560**, with 95% interval **[−0.001881, 0.000715]**. Thus this test does
not establish incremental benefit. Both lose to the pooled training-rate
benchmark on player MAE (**0.021221**). Opportunity Brier very slightly favors
tracking (**0.082383** versus **0.082393**); this small directional difference
does not resolve the weak player-level evidence.

![Figure 3. Traditional and tracking predictions for the 2025 OL holdout.](../outputs/figures/ol_predictions.png)

The earlier 2024 split has only 18 training and 19 test players. MAE is 0.026065
for traditional testing and 0.026146 for tracking. The 15%, 20% and 25% recovery
target variants all produce 54 eligible players; their 2025 improvement intervals
span zero. The results do not demonstrate stability or establish an optimal
recovery definition.

![Figure 4. Recovery-target sensitivity with paired test-player uncertainty.](../outputs/figures/lre_sensitivity.png)

For descriptive case studies, we selected the nearest 25th, 50th and 75th recovery
quantiles among guards, the most common eligible position, with ties broken by
player ID and no outcome-based selection. O'Cyrus Torrence, Dylan Fairchild and
Steve Avila have median delays of 0.60, 0.65 and 0.80 seconds. Their rookie
any-pressure rates are 7.34%, 6.02% and 8.79% across 613, 565 and 603 proxy
opportunities. Context differs; these examples illustrate measurements, not
validated player ordering. Only Fairchild belongs to the primary holdout.

## Separate receiver experiment

The preserved WR/TE model predicts rookie mean separation on regular-season
non-nullified routes, requiring at least 20 observed separation values. It uses
67 earlier-cohort training players and 27 held-out 2025 players. Traditional MAE
is 0.249064 and tracking MAE is 0.543811; R² falls from 0.398 to −2.893. The
paired MAE improvement interval is [−0.504741, −0.102434]. Broad drill features
perform poorly in this small temporal test. This negative result neither proves
nor disproves the offensive-line mechanism.

![Figure 5. The separate receiver-separation holdout.](../outputs/figures/receiver_predictions.png)

## Football implications and limitations

The current contribution is a transparent measurement and evaluation workflow,
with actual-frame comparisons and visible negative findings. It can support
research review. It does not support scouting adoption, causal coaching advice,
or a prospect ranking.

Before expanding claims, verify tracking units and drill phases, obtain independent
repeated attempts and body orientation, audit pressure attribution and timing,
incorporate football context, expand player cohorts, and evaluate prespecified
features externally. Small samples, selective completed recoveries, proxy
opportunities, informative censoring and fixed regularization remain material
limitations.

The accompanying notebook embeds the required source and recreates findings
with the official dataset attached, without a repository download. It was tested
locally from a fresh reproduction directory; Kaggle runtime execution remains
to be verified. The interactive local presentation is supporting material.
Original tracking and reconstructable exports remain private to the local
workspace. Verify current competition sharing terms before publishing figures.
