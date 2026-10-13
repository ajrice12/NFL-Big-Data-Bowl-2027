# Presentation redesign review

The previous local app and research exports were inspected before this redesign.
Its useful elements are the actual-frame playback, gap-aware derivatives,
mirror reversal/recovery events, temporal model outputs, censoring rules,
reproducible case selection, and distinct receiver experiment. These remain.
The eight-section navigation, large repeated headings, generic coordinate grid,
long algorithm panels, and first-load 480-attempt trajectory bundle obscure the
core question and the negative held-out result.

The redesign uses five sections: Overview, Movement, Metric, Results, Application.
Movement remains the centerpiece, with a code-drawn practice field, compact
athlete labels, live speed/acceleration, actual recovery events and rookie NFL
outcomes beside it. Field markings are schematic: the official Combine units
and physical field placement are unverified. Geometry uses one isotropic scale
and translation only; no invented opponents, body orientation or play context.
No reference logos or broadcast images are copied into the application.

The browser loads aggregate evidence first, then only selected attempts. The
source pipelines and existing scientific exports are retained. Detailed raw
samples and nine-method explanations move to expandable appendices. The first
screen states that candidate LRE has not established added predictive value.

## Delivered verification

64 real-browser checks pass across desktop, laptop and mobile viewports. The
initial screen contains the question, model cohort and primary negative finding.
The 24,832-byte briefing loads only the two featured attempts initially; the
catalog, individual trajectories and data appendix load when needed. Selected
athlete identities and actual frame timestamps were checked in the browser.
All 480 exported trajectories were independently matched to processed geometry,
speed and timestamps with `scripts.verify_presentation_export`. Five evidence
reports match source outputs. Re-running the scientific pipeline reproduced
all five analysis reports unchanged. The refreshed notebook also reproduces
all five reports locally; Kaggle runtime execution remains unverified.

Screenshots and machine-written reports: `outputs/verification/redesign/`.
Launch: `python -m scripts.serve --port 8765`.
Overview: `http://127.0.0.1:8765/presentation/#overview`.
Movement: `http://127.0.0.1:8765/presentation/#movement`.
