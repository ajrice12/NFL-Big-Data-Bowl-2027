# Verification record

Verified locally on 2026-10-12 (America/New_York), with Python 3.14.2 and installed
Microsoft Edge driven by Playwright. Generated reports and screenshots remain
in ignored `outputs/verification/`.

- **8 research edge-case tests passed:** stationary motion, known reversal and
  recovery, no reversal across a gap, translation invariance, timing censoring
  and invalid pressure times, minimum temporal cohort, nonfinite/conflicting
  tracking observations, and fractional player-ID rejection.
- **10 output checks passed:** preserved receiver score, positive completed
  recovery delays, censored incomplete delays, unique OL player-play keys,
  rookie REG cohort, role/rusher criteria, disjoint valid timing classes,
  invalid timing exclusion, and training/test cohort ordering and counts.
- **33 browser checks passed:** all chapters; two athletes; play/pause, scrub,
  speed, restart and drill controls; sample tables; all nine algorithm panels;
  recovery threshold examples; actual OL and distinct receiver results; case
  selection; five mobile chapter overflow checks; missing-data failure state;
  no execution/console errors; no failed app resources; raw CSV requests refused.
- **Notebook reproduced locally:** 8 executable code cells completed from the
  five official CSVs in a fresh output directory. Receiver model, OL model,
  movement, outcome and sensitivity reports match the workspace exactly.
  Execution on Kaggle's runtime has not been verified.
- **Visual review:** opening, laboratory, algorithm, findings and conclusion
  screenshots inspected, along with all five generated scientific figures.
  Comparison GIF contains 99 recorded-time frames at 100 ms each.

The browser report is written by the test, not a manual success flag. Missing
export is simulated with an intercepted 404; its expected error is isolated
from the normal-load console/resource checks. Screenshots disable CSS entry
transitions to capture fully visible content. The server remains on loopback
for the requested live viewing session; stop its terminal with Ctrl+C.

These checks verify implementation and local reproducibility. They do not
validate LRE's football interpretation, independent repeatability, survival
assumptions, or competition publication permissions.
