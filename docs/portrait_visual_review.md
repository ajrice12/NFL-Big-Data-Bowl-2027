# Season portraits and movement visual update

Player identities now use actual historical-roster headshots in the overview,
guided film and comparison, research scorebug and NFL sidebar, methodology
example, named data/prediction tables, and expandable OL/receiver holdout lists.
The movement labels themselves also show cached portrait thumbnails. Native
select menus retain text; the added photo gallery selects either athlete's
actual recorded attempt without replacing the original controls.

## Source matching and limits

The optional `python -m scripts.build_portraits` command retrieves nflverse
rosters for 2023–2025 and uses each player's draft/rookie season. Tracking NFL
IDs match roster `gsis_it_id`; roster `headshot_url` points to the image source.
Sources are the maintained
[nflverse roster releases](https://github.com/nflverse/nflverse-data/releases/tag/rosters)
and their NFL image URLs. No current-season image is substituted for a missing
historical one. [Roster tooling documentation](https://github.com/nflverse/nflverse-rosters)
describes the release source.

480 of the 510 dataset players have retrieved season-associated photos. Thirty
use an explicit NO PHOTO/initials placeholder: 28 lack a unique usable seasonal
URL and two lack a matching season roster ID. All three featured guards have
photos for the correct rookie roster year. The source establishes roster-season
association, not the exact photo capture date; labels and tooltips state this.

Some source birth dates disagree. A conflicting birth date is accepted for
portrait identity only if the exact numeric NFL ID and normalized full name
(including permitted Jr./Sr. suffix normalization) agree; the discrepancy is
recorded in the local manifest. Scientific player metadata is never corrected
or overwritten by this display operation.

Roster snapshots, portrait images, URLs and hashes are local ignored outputs in
`outputs/presentation/`. The public repo stores the builder and presentation
code, not the photographic cache. The source data's software license does not
establish redistribution rights for the photographs. This update does not
publish a photo collection or imply league endorsement.

## Animation changes

The original top-down practice diagram now has cached grass texture, subtle
mowing bands, shaded equipment, white boundaries and hash paint. Paint/equipment
remain illustrative; no yard dimensions, surveyed cone positions or NFL game
footage are claimed. The isotropic coordinate mapping and actual timestamps
are unchanged. The source-unit scale remains explicit and legible against a
dark backing.

Large tabular-numeral elapsed-time clocks appear above and inside the animation.
They track the same recorded elapsed time as the original scrubber, including
quarter-speed replay. The clock is Combine elapsed time, not NFL protection time.
Portrait image nodes and decoded canvas bitmaps are reused during playback;
the grass background is rendered once per canvas size.

## Verification

26 new browser checks cover real photo decoding, season identity, photo-picker
selection, comparison, stable image nodes, large-timer synchronization and size,
unavailable-photo fallback, OL/receiver holdout lists and responsive layouts.
The existing 63 story checks and 64 research checks still pass. All 480 images
were decoded and their hashes and exact season-roster source URLs/IDs verified.
No normal-load image or JavaScript failures occurred. Screenshots were visually
reviewed at 1440×900 and 1366×768; 390×844 layout checks also pass. Local reports
and screenshots are under `outputs/verification/portraits/`.

No research model, feature calculation, outcome definition or data selection
was changed.
