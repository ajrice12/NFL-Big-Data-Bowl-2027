# Do Combine movement traits translate to rookie receiving separation?

**Status: exploratory draft. Results and conclusions have not been established.**

## Football question

Can movement traits measured during Combine drills add information beyond
traditional Combine tests when evaluating rookie WR/TE separation at pass-forward?
The potential use is to identify development questions for scouts and coaches.

## Data and methods

Use official Combine PLAYER tracking, traditional Combine results, player metadata,
game metadata, and player-play outcomes. Derive signed acceleration from speed
only across consecutive approximately 10 Hz frames. Summarize each attempt and
take medians across attempts within each named drill. Keep drill identities separate.

Limit outcomes to non-nullified regular-season plays in each player's draft year,
WR/TE players with recorded routes, and at least 20 observed separation values.
Compare a traditional-test ridge model with a model adding sensor traits. Train on
earlier draft cohorts and hold out the latest cohort. Fit imputers and scalers on
training players only. Report player counts, MAE, R², and paired bootstrap
uncertainty in the change in MAE. Compare against the training-outcome mean.

## Results to complete

- Report cohort and drill coverage, missingness, and exclusions.
- Insert verified model comparisons and the held-out error figure.
- Select a position-specific drill hypothesis before confirmatory analysis.
- Check sensitivity to opportunity thresholds, drill availability, and role.

## Limits and next steps

Separation depends on deployment, route, coverage, quarterback timing, and which
plays have observed tracking. This starter model does not yet adjust for those
contexts. Missing drill participation may encode selection. One held-out cohort
does not establish stability across years. The bootstrap covers held-out players,
not uncertainty from refitting. Confirm coordinate and speed units against the
official data dictionary before interpreting magnitudes. Game tracking files are
available but the initial model uses supplied play-level separation; deriving
additional in-game movement outcomes is future work. Career totals are deliberately
excluded because exposure differs across draft classes.

## Submission checklist

Based on the supplied competition page excerpt: link Combine sensor data to NFL
performance; stay within 2,000 words and fewer than 10 tables/figures; attach a
public Kaggle Notebook. Recheck current competition requirements before submission.
