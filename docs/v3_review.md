# V3 football storytelling review

The prior five-section app exposed cohort counts, feature definitions and
model results before viewers had an opportunity to watch an athlete. V3 adds a
separate guided experience and preserves the complete analytical interface.

## Delivered experience

The entry route is `#story`: competition identity, title, a single question,
Watch the Breakdown, and Explore the Research. An actual featured trajectory
appears on an original schematic field behind the title. The introduction lasts
about two seconds and navigation is immediately available. No looping background
motion or mandatory loading sequence was added.

Five self-paced scenes introduce the problem, watch Torrence's movement,
measure his first reversal, show the verified OL finding, and explain scouting
limits. Approximate viewing length is 60–90 seconds, depending on reading and
replay time; this is an editorial estimate, not a timed usability-study result.
Back, Next, Skip to Results and a five-part progress strip guide the viewer.

Player Film autoplays the featured attempt, briefly slows its first recorded
reversal to quarter speed and annotates the event. The displayed source clock
also advances at quarter speed; coordinates are never interpolated. A small
temporary camera zoom emphasizes the event. Replay restarts the actual attempt.
Compare Players fetches Avila only on request and uses shared isotropic geometry
in two synchronized fields. Names, position, year, drill, ID, attempt and live
reported speed appear in broadcast lower-thirds. The observed reset delay
appears after the target is reached. The metric scene explains the definition.

Research Tools retains filters, drills, trail encodings, the time series, target
sensitivity, all nine methodology steps, local sample exploration, models,
coefficients, uncertainty intervals, outliers and the separate receiver study.
No scientific algorithm, dataset or fitted model was changed. The OL study was
already implemented and verified before this redesign; it is not a proposed
study being presented as completed. Its main finding remains inconclusive.

The palette is navy, white, restrained electric blue and red, with field green
reserved for movement. Locally licensed Barlow Condensed, Oswald and Inter replace
the system-only typography. Chapter changes use short angled wipes; reduced
motion disables transitions and autoplay. Plain typographic NFL identification
is the requested logo fallback, with independent-research labeling. See asset
credits for source and license details.

## Verification

- 52 guided browser checks passed at 1440×900, 1366×768, 1280×800 and 390×844.
- All 64 retained research browser checks passed, including 1920×1080.
- No normal-load script errors or failed assets in the final test runs.
- Play, pause, replay, actual-frame scrubbing, quarter-speed reversal, compare
  toggle, measurement seek, navigation, evidence expansion and lazy loading pass.
- Reduced motion leaves manual playback available without autoplay.
- Missing trajectories disable film controls and display an explicit error.
  Existing missing briefing/model/attempt checks and raw-data blocking still pass.
- The exporter verifier again confirms all 480 exported trajectories and five
  evidence objects match their processed-source data and analysis reports.
- Captured and visually reviewed opening, player film, comparison, measurement,
  findings, scouting implications, Research Tools, laptop film and mobile opening.
  Local screenshots/reports are in `outputs/verification/v3/`.

Review corrections: await asynchronous comparison/navigation before asserting
their results; replace a horizontal chapter slide with an angled wipe to avoid
transient overflow; move the recovery target label away from the player label.

## Local launch

From the repository root:

```powershell
.\.venv\Scripts\python.exe -m scripts.serve --port 8765
```

Open http://127.0.0.1:8765/presentation/#story. The loopback server must remain
running. Raw tracking data and all generated local exports stay out of Git.
