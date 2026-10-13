# Football question review: verification and comprehension assessment

## Verified scope

The presentation is now **The Pass-Protection Test**. The initial assessment was
written before implementation in `docs/scientific_story_assessment.md` and
summarized to the user. The five guided scenes now follow the football question,
verified finding, timing distinction, Combine hypothesis and scouting implications.
The former reset-measurement chapter is an optional detour, with full mathematics
retained in Research Tools. Existing analytical hash URLs remain supported.

No file in `src/` changed, no model was refitted and no outcome was relabeled.
The notebook generator and notebook changed their markdown title only; every
executable notebook cell was compared and is unchanged. The writeup question and
README were synchronized to the actual outcome. Historical V3 review records
are retained as history, not current descriptions.

## Source checks

The processed opportunities table reproduces 23,768 player-play opportunities:
1,373 pressure by 3 seconds, 8,833 clean through 3, 13,490 pressure-free earlier
endings, and 72 invalid/missing pressure times. The classification is mutually
exclusive and exhaustive after including timing exclusions. Of the 2,202 total
pressure observations, 757 have valid times later than 3 seconds and belong to
the clean-through-checkpoint group. These are player-play counts, not unique
game-play counts. The descriptive group includes 81 rookies, while model
eligibility leaves 54; the presentation identifies this difference.

`scripts.verify_presentation_export` again confirms all five evidence objects
match source analysis reports and all 480 trajectories match processed tracking.
The model still predicts overall pressure rate. A separately specified future
three-second study is proposed in the assessment; it was not implemented.

## Browser review

63 scientific-story checks and 64 retained research checks pass, with no
normal-load script errors or failed assets. Browser checks include title and
question, finding-first navigation, time classification counts, three illustrative
ending selectors, explicit model-horizon limitation, contextual Combine framing,
actual-frame scrub/speed, quarter-speed reversal, comparison, reset seek, replay,
all research tools, missing data, reduced motion and responsive layouts.

Screenshots in `outputs/verification/question-review/` include the opening,
findings, timing, player movement, comparisons, optional metric and Research Tools
at 1440×900. All guided scenes and the optional metric/research overview were
also captured at 1366×768. Both requested sizes were visually reviewed. The
required question and headline finding are visible without expanding any details.
Additional 1280×800 and 390×844 checks pass. Screenshot capture uses full-page
images, so longer scenes show material below the initial viewport as well.

Football game diagrams and timeline paths are explicitly illustrative, not
real NFL tracking. Actual Combine movement uses a separate practice diagram;
its grid and equipment positions are illustrative. No game yard numbers,
endzones, opponent traces or inferred contact measurements are drawn. Geometry,
timing and data selection remain unchanged.

## Sixty-second editorial walkthrough

This is an editorial review, not a participant-based usability study or a claim
that every first-time viewer will understand the material in sixty seconds.

| Approximate viewing budget | Information the story makes available |
|---|---|
| 0–15 s: opening | A blocker must react to a rusher. The question is whether Combine recovery helps predict rookie pressure allowed. |
| 15–30 s: immediate finding | Adding recovery has not established improved prediction. This is an overall-rate model, not a three-second model. |
| 30–50 s: timing distinction | Pressure by 3, clean through 3, and an early-ending unknown are different observations. A clean short opportunity does not establish sustained protection. |
| 50–60 s: Combine hypothesis | A reset could be relevant to reacting to a rush move, but the drill omits contact/assignments/QB context and the cohort result remains inconclusive. |

Expected plain-language explanation after this walkthrough:

> We tested whether recovering after a Combine direction change helps predict
> rookie pressure allowed beyond traditional tests. It has not shown added value.
> We can describe observations at three seconds, but we have not fitted a model
> of protection lasting that long, and early clean endings leave that outcome unknown.

Assessment: the revised sequence supports that explanation and exposes the
finding before any metric formula. Real-viewer testing remains unperformed;
ask future reviewers those three questions before showing Research Tools:
What was predicted? Did recovery help? What can an early clean ending tell us?
