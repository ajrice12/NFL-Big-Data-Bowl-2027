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

## Football presentation redesign verification

The five-section redesign was verified on 2026-10-12 EDT / 2026-10-13 UTC.
The original eight-section screenshots and reports are preserved locally; latest
artifacts are in `outputs/verification/redesign/`.

- **64 browser checks passed** in real Edge/Playwright, with zero normal-load
  JavaScript/console errors or failed resource requests. All five sections were
  checked at 1366×768, 1920×1080, 1280×800 and 390×844 without page overflow.
- The first screen exposes the cohort counts and main finding without scrolling.
  Startup fetches a 24,832-byte briefing and two selected trajectory files, not
  the full 480-attempt bundle, catalog or sample appendix. One measured local
  browser startup was 614 ms; that is an observation, not a performance guarantee.
- Actual names, NFL IDs, attempt IDs and scrubbed frame timestamps match source
  metadata. Overlay/split fields, replay, speed, trail encodings, and metric
  reversal/target controls passed. Isotropic shared scale and translation-only
  geometry were checked; a synthetic gap test confirms no interpolation.
- Missing briefing, missing OL model results and unavailable selected tracking
  each produce explicit incomplete/unavailable states. Playback disables when
  the selected tracking cannot load. Raw CSV requests remain blocked.
- **All 480 trajectory exports** were compared against processed x/y/s and
  timestamps. Five evidence objects match the rounded source JSON reports.
  The full research pipeline reproduced all five analysis reports unchanged.
- The eight research edge-case tests and ten cohort/output checks still pass.
  The rebuilt self-contained notebook completed all eight executable cells
  locally; all five analysis reports matched again. Kaggle runtime is untested.
- Screenshots of Overview, Movement, Metric, Findings and Application were
  captured and visually inspected. Reference assets and official/team logos
  were not copied. The field is an original code-drawn schematic.

No research algorithm was replaced for this visual change. OL and receiver
hypotheses remain separate. Field yard labels are visual context; the actual
Combine scale is stated in source units because the dictionary is unverified.
The live loopback server is retained for the user's viewing request.


## V3 guided sports presentation

The default entry is now a five-scene football story with Research Tools as an
optional analytical mode. 52 new browser checks and all 64 research regression
checks pass. The final runs have no normal-load script or asset failures.
Source-export verification again confirms 480 attempts and five evidence
objects. Screenshots and reports: `outputs/verification/v3/`. Full review and
launch instructions: `docs/v3_review.md`. Research algorithms are unchanged.


## Scientific question and viewer review (current)

The presentation is now The Pass-Protection Test. This supersedes V3's title
and guided scene order; the research remains unchanged. The initial assessment
is in `docs/scientific_story_assessment.md`. The outcome audit reproduces all
23,768 player-play opportunities and their disjoint checkpoint categories.
63 story checks plus 64 research checks pass. Requested 1440x900 and 1366x768
screenshots were reviewed. The sixty-second comprehension judgment is editorial,
not a participant study. See `docs/question_review_verification.md` and local
`outputs/verification/question-review/` screenshots/reports. All 480 exported
trajectories still match processed source data.
